import django_filters
from .models import Order


class OrderFilter(django_filters.FilterSet):
    user = django_filters.CharFilter(field_name='user__profile__name', lookup_expr='icontains')
    status = django_filters.ChoiceFilter(field_name='status', choices=Order.ORDER_STATUS_CHOICES)

    class Meta:
        model = Order
        fields = ["status", "user"]