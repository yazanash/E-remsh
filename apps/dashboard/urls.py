from django.urls import path
from . import views
from django.urls import path
from .views import UserSignUpAPIView, CustomLoginAPIView

urlpatterns = [
    path('signup/', UserSignUpAPIView.as_view(), name='signup'),
    path('login/', CustomLoginAPIView.as_view(), name='login'),
    path('', views.home, name='home'),
    # path('products/', views.list_product, name='products_list'),
    # path('products/create/', views.create_product, name='product_create'),
]
