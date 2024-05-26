from django_filters.filterset import FilterSet, CharFilter
from django.db.models import Q

from .models import ProductsModel


class ProductsFilterSet(FilterSet):
    search = CharFilter(method='search', label='Search')

    class Meta:
        model = ProductsModel
        fields = []

    def search(self, queryset, name, value):
        return queryset.filter(
            Q(title__icontains=value) | Q(utils__icontains=value) |
            Q(description__icontains=value) | Q(category_id__category__icontains=value)
        )

