from rest_framework import serializers
from .models import User, OTP, Customer


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
        model = Customer
        fields = ['name', 'gender', 'phone', 'birthdate']



class UserSerializer(serializers.ModelSerializer):
    group = serializers.SerializerMethodField()  # Fetch the user's group name
    profile_name = serializers.CharField(source='username')  # Fetch the profile name from username

    class Meta:
        model = User
        fields = ['email', 'group', 'profile_name']  # Specify the fields to return

    def get_group(self, obj):
        # Ensure only one group is returned (assuming the user has only one group)
        group = obj.groups.first()  # Fetch the first (and only) group
        return group.name if group else None