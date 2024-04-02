from django_filters import rest_framework as filters
from .models import Refer


class ReferFilter(filters.FilterSet):
    min_date = filters.DateFilter(field_name="expire_date", lookup_expr = 'gte')
    max_date = filters.DateFilter(field_name = 'expire_date', lookup_expr = 'lte')

    class Meta:
        model = Refer
        fields = ('created_date', 'expire_date')