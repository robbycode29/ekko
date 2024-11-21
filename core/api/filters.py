import django_filters
from core.models import Product

class ProductFilter(django_filters.FilterSet):
    title = django_filters.CharFilter(field_name='title', lookup_expr='icontains')
    price = django_filters.NumberFilter(field_name='price', lookup_expr='icontains')
    stars = django_filters.NumberFilter(field_name='stars', lookup_expr='icontains')
    reviews = django_filters.NumberFilter(field_name='reviews', lookup_expr='icontains')

    class Meta:
        model = Product
        fields = ['title', 'price', 'stars', 'reviews']