from rest_framework import serializers
from .models import User, OTP,Customer

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['email']

class OTPSerializer(serializers.ModelSerializer):
    class Meta:
        model = OTP
        fields = ['email', 'otp_code']
    
class CustomerSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['name','gender','phonenumber','birthdate','user']