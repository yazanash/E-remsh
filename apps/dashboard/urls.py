from django.urls import path
from . import views
from django.urls import path
from .views import UserSignUpView, CustomLoginView

urlpatterns = [
    path('signup/', UserSignUpView.as_view(), name='signup'),
    path('login/', CustomLoginView.as_view(), name='login'),
    path('', views.home, name='home'),
    path('products/', views.list_product, name='products_list'),
    path('products/create/', views.create_product, name='product_create'),
]
