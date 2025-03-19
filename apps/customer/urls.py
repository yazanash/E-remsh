from django.urls import path
from .views import *
from rest_framework_simplejwt.views import (
    TokenRefreshView,
    TokenVerifyView,
)

urlpatterns = [
    path('customer/send-otp/', SendOTPView.as_view(), name='send_otp'),
    path('customer/verify-otp/', VerifyOTPView.as_view(), name='verify_otp'),
    path('customer/profile/', UserProfileView.as_view(), name='create_profile'),
    path('token/access/', TokenRefreshView.as_view(), name='token_refresh'),
    path('token/verify/', TokenVerifyView.as_view(), name='token_verify'),
    path('token/refresh/', RefreshRefreshTokenView.as_view(), name='refresh_refresh_token'),

    path('signup/', UserSignUpAPIView.as_view(), name='signup'),
    path('login/', CustomLoginAPIView.as_view(), name='login'),
    path('get-admins/', get_admins, name='get_users'),
    path('user-group/', get_user_group, name='get_user_group'),

    path('admins/add/', add_user_to_admins, name='add_admin'),
    path('admins/change/<str:user_id>/', change_user_group, name='change_user_group'),
    path('admins/remove/<str:user_id>/', remove_user_from_admins, name='remove_user_group'),

]
