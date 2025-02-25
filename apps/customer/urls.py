from django.urls import path
from .views import SendOTPView, VerifyOTPView, UserProfileView

urlpatterns = [
    path('customer/send-otp/', SendOTPView.as_view(), name='send_otp'),
    path('customer/verify-otp/', VerifyOTPView.as_view(), name='verify_otp'),
    path('customer/profile/', UserProfileView.as_view(), name='create_profile'),
]