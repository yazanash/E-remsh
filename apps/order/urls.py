from django.urls import path
from . import views


urlpatterns = [
    path('orders/create/', views.create_order, name="create_order"),
    path('orders/', views.get_orders, name="get_order"),
    path('orders/get/<str:order_id>/', views.get_order_by_id, name="get_order"),
    path('orders/get-all/', views.get_all_orders, name="get_all_order"),
    path('orders/status/<str:order_id>/', views.update_order_status, name="update_order_status"),
    path('orders/delete/<str:order_id>/', views.delete_order, name="delete_order"),

    path('delivery/', views.get_delivery_offices, name="get_delivery_offices"),
    path('delivery/create/', views.create_delivery, name="get_delivery_offices"),
    path('delivery/<str:delivery_id>/edit/', views.edit_delivery, name="get_delivery_offices"),

    path('coupons/', views.get_coupons, name="get_delivery_offices"),
    path('coupons/create/', views.create_coupon, name="get_delivery_offices"),
    path('coupons/<str:coupon_id>/edit/', views.edit_coupon, name="get_delivery_offices"),
]
