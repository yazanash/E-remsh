from django.urls import path
from . import views
from .views import ProductView

urlpatterns = [
    path('products/', ProductView.as_view(), name="products"),
    path('products/<str:product_id>/', views.get_product_by_id, name="products.get"),
    # path('products/', views.create_product, name='create_products'),
    path('categories/', views.get_categories,name="categories"),


    path('products/<str:product_id>/like/', views.like_product, name='like_product'),
    path('products/<str:product_id>/unlike/', views.unlike_product, name='unlike_product'),

    path('products/<str:product_id>/wishlist/', views.add_to_wishlist, name='add_to_wishlist'),
    path('products/<int:product_id>/wishlist/remove/', views.remove_from_wishlist, name='remove_from_wishlist'),
    path('wishlist/', views.get_wishlist, name='get_wishlist'),
]
