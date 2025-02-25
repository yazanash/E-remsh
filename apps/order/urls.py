from django.urls import path
from . import views


urlpatterns = [
    path('orders/create/', views.create_order, name="create_order"),
    path('orders/', views.get_orders, name="get_order"),
    path('orders/status/<str:order_id>', views.update_order_status, name="update_order_status"),
    path('orders/delete/<str:order_id>', views.delete_order, name="delete_order"),
    path('offices/', views.get_delivery_offices, name="get_delivery_offices"),
]
