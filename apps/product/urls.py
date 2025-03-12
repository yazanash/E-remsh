from django.urls import path
from . import views
from .views import ProductView

urlpatterns = [
    path('products/', ProductView.as_view(), name="products"),
    path('products/<str:product_id>/', views.get_product_by_id, name="products.get"),
    path('products/<str:product_id>/edit/', views.edit_product, name="products.edit"),
    path('products/<str:product_id>/items/add/', views.add_item, name="products.add_item"),
    path('products/items/delete/<str:item_id>/', views.delete_item, name="products.delete_item"),
    # path('products/', views.create_product, name='create_products'),
    path('categories/', views.get_categories,name="categories"),
    path('products/images/add/', views.add_image,name="add_image"),
    path('products/images/edit/<str:image_id>/', views.edit_image, name="edit_image"),
    path('products/images/delete/<str:image_id>/', views.delete_image, name="delete_image"),


    path('products/<str:product_id>/like/', views.like_product, name='like_product'),
    path('products/<str:product_id>/unlike/', views.unlike_product, name='unlike_product'),

    path('products/<str:product_id>/wishlist/', views.add_to_wishlist, name='add_to_wishlist'),
    path('products/<str:product_id>/wishlist/remove/', views.remove_from_wishlist, name='remove_from_wishlist'),
    path('wishlist/', views.get_wishlist, name='get_wishlist'),
]
