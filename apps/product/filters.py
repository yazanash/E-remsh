import django_filters
from .models import Product

class ProductFilter(django_filters.FilterSet):
    category = django_filters.CharFilter(field_name='category__name', lookup_expr='iexact')
    keyword = django_filters.CharFilter(field_name='name', lookup_expr='icontains')
    class Meta:
        model=Product
        fields=["name","category","keyword"]