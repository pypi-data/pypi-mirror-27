TEXT_LOOKUPS = [
    'exact', 'iexact', 'in', 'contains', 'icontains', 'startswith',
    'istartswith', 'endswith', 'iendswith', 'regex', 'iregex'
]

CHOICES_LOOKUPS = ['exact', 'in']
RANGE_LOOKUPS = ['exact', 'gt', 'gte', 'lt', 'lte']

DATETIME_LOOKUPS = RANGE_LOOKUPS + \
    ['date__' + lookup for lookup in RANGE_LOOKUPS] + \
    ['year', 'month', 'week_day', 'day', 'hour']
