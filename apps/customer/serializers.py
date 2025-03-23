import datetime

from rest_framework import serializers
from .models import User, OTP, Customer


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['email', 'device_token']


class OTPSerializer(serializers.ModelSerializer):
    class Meta:
        model = OTP
        fields = ['email', 'otp_code']


class CustomerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customer
        fields = ['name', 'gender', 'phone', 'birthdate']


class UserDashboardSerializer(serializers.ModelSerializer):
    password2 = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['email', 'password', 'password2']
        extra_kwargs = {'password': {'write_only': True}}

    def validate(self, data):
        if data['password'] != data['password2']:
            raise serializers.ValidationError("Passwords do not match.")
        return data

    def create(self, validated_data):
        validated_data.pop('password2')
        if not validated_data.get('username'):
            timestamp = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
            validated_data['username'] = f"{validated_data['email'].split('@')[0]}-{timestamp}"
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password']
        )
        return user


class CustomAuthenticationFormSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)


class UserDataSerializer(serializers.ModelSerializer):
    group = serializers.SerializerMethodField()  # Fetch the user's group name
    name = serializers.CharField(source='profile.name', allow_null=True)  # Fetch the profile name from username

    class Meta:
        model = User
        fields = ['id','email', 'group', 'name']  # Specify the fields to return

    def get_group(self, obj):
        # Ensure only one group is returned (assuming the user has only one group)
        group = obj.groups.first()  # Fetch the first (and only) group
        return group.name if group else None