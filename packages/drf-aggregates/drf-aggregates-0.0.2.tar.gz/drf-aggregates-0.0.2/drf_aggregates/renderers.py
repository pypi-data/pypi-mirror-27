from rest_framework import renderers

from django.db.models import Case, CharField, Value, When
from django.db.models.aggregates import Aggregate, Avg, Count, Max, Min, StdDev, Sum, Variance
from django.db.models.functions import Extract

from .aggregates import CountFalse, CountTrue

AGGREGATE_FNS = {
    # default django functions
    'Aggregate': Aggregate,
    'Avg': Avg,
    'Count': Count,
    'Max': Max,
    'Min': Min,
    'StdDev': StdDev,
    'Sum': Sum,
    'Variance': Variance,
    # custom aggergate functions
    'CountTrue': CountTrue,
    'CountFalse': CountFalse,
}


class AggregateRenderer(renderers.BaseRenderer):
    """
    """
    media_type = 'application/json'
    format = 'agg'

    def _clean_agg_query_params(self, query_params, keyword):
        """
        Checks the supplied query_params object for keys containing the supplied keyword
        and parses the query_params to return a dictionary of arg: value where the query_param
        is keyword[arg]=value. Handles multiple instances of keyword[arg].
        """
        try:
            cleaned_matches = {
                key[key.index('[') + 1: key.index(']')]: query_params.getlist(key)
                for key in query_params.keys() if keyword in key
            }
        except ValueError as e:
            cleaned_matches = {}
        return cleaned_matches

    def render(self, data, media_type=None, renderer_context=None):
        """
        Render queryset into its aggregate representation using the requested functions,
        and custom behaviour if defined on the queryset.
        Returns in a dictionary with results under the key 'data'
        """
        if 'queryset' in data:
            query_args = {}
            if 'request' in data:
                request = data['request']
                query_args = {
                    key: self._clean_agg_query_params(request.query_params, key)
                    for key in ('aggregate', 'group_by')
                }

            qs = data['queryset']
            keys = []

            if query_args.get('group_by'):
                group_keys = []

                # special rules on how to handle fields
                for field in query_args['group_by'].keys():
                    qs, processed_field = self.process_group_by(qs, field)
                    group_keys.extend([field, processed_field])

                qs = qs.values(*group_keys).order_by(*group_keys)
                keys.extend(group_keys)

            if query_args.get('aggregate'):
                aggs = {}
                custom_functions = {}

                for fn_name, fn_args in query_args['aggregate'].items():
                    # annotate with the aggregation requested
                    for fn_arg in fn_args:
                        try:
                            # aggregate function requested is a default
                            agg_fn = AGGREGATE_FNS[fn_name]
                        except KeyError:
                            # aggregate function requested will be passed on
                            # to the queryset's custom_aggregates method
                            custom_functions[fn_name] = fn_arg
                        else:
                            key = f'{fn_name}_{fn_arg}'.lower()
                            aggs[key] = agg_fn(fn_arg)
                            keys.append(key)

                # if a custom method exists, call it
                # expect it to return a dictionary of aggregate functions
                if hasattr(qs, 'calculate_aggregates'):
                    custom_aggs = qs.calculate_aggregates(**custom_functions)
                    aggs = {**aggs, **custom_aggs}
                    keys.extend(custom_aggs.keys())

                if aggs:
                    qs = qs.annotate(**aggs) if query_args.get('group_by') else qs.aggregate(**aggs)

            result = list(qs.values(*keys)) if not isinstance(qs, dict) else qs
            result = {'data': result}
            return result

        return data

    def process_group_by(self, qs, field):
        """
        Custom behaviour for field types.
        ChoiceFields will return an additional field with _display that contains the display value
        DateFields have the ability to be grouped by an extracted part (i.e. year, month, day)
        Returns the annotated queryset and field name to be used for the group_by.
        """
        field_name = field

        # get the django model field definition
        model_field = qs.model._meta.get_field(field.split('__')[0] if '__' in field else field)

        # choices should display the human readable string
        if hasattr(model_field, 'choices') and model_field.choices:
            whens = [
                When(**{field: value, 'then': Value(value_repr)})
                for value, value_repr in model_field.choices
            ]
            field_name = f'{field}_display'
            qs = qs.annotate(**{
                field_name: Case(*whens, default=Value(''), output_field=CharField())
            })

        # dates
        elif model_field.__class__.__name__ in ('DateTimeField', ):
            datefield, part = field.split('__')
            if part:
                qs = qs.annotate(**{
                    field_name: Extract(datefield, part)
                })

        return qs, field_name
