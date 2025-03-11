from django.urls import path
from .views import SendOTPView, VerifyOTPView, UserProfileView
from rest_framework_simplejwt.views import (
    TokenRefreshView,
    TokenVerifyView,
)


urlpatterns = [
    path('customer/send-otp/', SendOTPView.as_view(), name='send_otp'),
    path('customer/verify-otp/', VerifyOTPView.as_view(), name='verify_otp'),
    path('customer/profile/', UserProfileView.as_view(), name='create_profile'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('token/verify/', TokenVerifyView.as_view(), name='token_verify'),
]