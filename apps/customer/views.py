from django.contrib.auth import authenticate, login
from django.contrib.auth.models import Group
from django.shortcuts import render, get_object_or_404
from rest_framework.decorators import api_view
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.core.mail import send_mail
from .models import User, OTP, Customer
from .serializers import UserSerializer, OTPSerializer, CustomerSerializer, UserDataSerializer, \
    CustomAuthenticationFormSerializer, UserDashboardSerializer
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.exceptions import TokenError
import random
from rest_framework.permissions import IsAuthenticated


# Create your views here.
class SendOTPView(APIView):
    def post(self, request):
        email = request.data.get('email')
        otp_code = str(random.randint(100000, 999999))
        OTP.objects.create(email=email, otp_code=otp_code)

        send_mail(
            'Your OTP Code',
            f'Your OTP code is {otp_code}',
            'from@example.com',
            [email],
        )
        return Response({'message': 'OTP sent'}, status=status.HTTP_200_OK)


class VerifyOTPView(APIView):
    def post(self, request):
        email = request.data.get('email')
        otp_code = request.data.get('otp_code')
        otp = OTP.objects.filter(email=email, otp_code=otp_code).first()
        if otp and otp.is_valid:
            otp.is_valid = False
            otp.save()
            exist_user = User.objects.filter(email=email).first()
            if exist_user is None:
                serializer = UserSerializer(data=request.data)
                if serializer.is_valid():
                    user = serializer.save()
                    refresh = RefreshToken.for_user(user)
                    customer_group, _ = Group.objects.get_or_create(name='customer')
                    user.groups.add(customer_group)
                    return Response({
                        'message': 'User registered',
                        'refresh': str(refresh),
                        'access': str(refresh.access_token),
                    }, status=status.HTTP_201_CREATED)
                else:
                    return Response({'message': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
            else:
                exist_user.device_token = request.data['device_token']
                exist_user.save()
                refresh = RefreshToken.for_user(exist_user)
                return Response({
                    'message': 'User registered',
                    'refresh': str(refresh),
                    'access': str(refresh.access_token),
                }, status=status.HTTP_201_CREATED)
        else:
            return Response({'message': 'Invalid OTP'}, status=status.HTTP_400_BAD_REQUEST)


class UserProfileView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = CustomerSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user)
            return Response({'data': serializer.data}, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def get(self, request):
        user = request.user
        customer = get_object_or_404(Customer, user=user)
        serializer = CustomerSerializer(customer,many=False)
        return Response({"data": serializer.data}, status=status.HTTP_200_OK)

    def put(self, request):
        user = request.user
        customer = get_object_or_404(Customer, user=user)
        serializer = CustomerSerializer(customer,data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user)
            return Response({'data': serializer.data}, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class RefreshRefreshTokenView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        # Extract the existing refresh token from the request
        refresh_token = request.data.get('refresh')
        if not refresh_token:
            return Response({"message": "Refresh token is required."}, status=status.HTTP_400_BAD_REQUEST)

        try:
            # Verify and blacklist the old refresh token
            old_refresh = RefreshToken(refresh_token)
            old_refresh.blacklist()  # Requires token blacklisting to be enabled

            # Create a new refresh token
            new_refresh = RefreshToken.for_user(request.user)
            user = request.user
            user.device_token = request.data['device_token']
            user.save()
            return Response({"refresh": str(new_refresh)}, status=status.HTTP_200_OK)
        except TokenError as e:
            return Response({"message": "Invalid or expired refresh token."}, status=status.HTTP_400_BAD_REQUEST)


# Create your views here.
class UserSignUpAPIView(APIView):
    def post(self, request, *args, **kwargs):
        serializer = UserDashboardSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            login(request, user)
            refresh = RefreshToken.for_user(user)
            user_serializer = UserDataSerializer(user, many=False)
            return Response({
                "message": "User created and logged in successfully",
                "access": str(refresh.access_token),
                "refresh": str(refresh),
                "user": user_serializer.data
            }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CustomLoginAPIView(APIView):

    def post(self, request, *args, **kwargs):
        serializer = CustomAuthenticationFormSerializer(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data['email']
            password = serializer.validated_data['password']
            user = authenticate(request, username=email, password=password)
            if user is not None:
                login(request, user)
                refresh = RefreshToken.for_user(user)
                user_serializer=UserDataSerializer(user, many=False)
                return Response({
                    "message": "User logged in successfully",
                    "access": str(refresh.access_token),
                    "refresh": str(refresh),
                    "user": user_serializer.data
                }, status=status.HTTP_200_OK)
            return Response({"error": "Invalid email or password"}, status=status.HTTP_401_UNAUTHORIZED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
def get_admins(request):
    # Get the "Customer" group
    customer_group = Group.objects.get(name='customer')
    # Filter users who are not in the "Customer" group
    users = User.objects.exclude(groups=customer_group)
    serializer = UserDataSerializer(users, many=True)
    return Response({'data': serializer.data})


@api_view(['GET'])
def get_user_group(request):
    serializer = UserDataSerializer(request.user, many=False)
    return Response({'data': serializer.data})


@api_view(['POST'])
def add_user_to_admins(request):
    try:
        email = request.data['email']
        group_name = request.data['group']
        if not email or not group_name:
            return Response({'error': 'Email and group name are required.'}, status=status.HTTP_400_BAD_REQUEST)
        # Get user by email
        user = User.objects.get(email=email)
        # Get or create the group
        group = Group.objects.get(name=group_name)
        # Clear user's current groups and assign the new one
        user.groups.clear()
        user.groups.add(group)
        serializer = UserDataSerializer(user, many=False)
        return Response({'data': serializer.data}, status=status.HTTP_200_OK)
    except User.DoesNotExist:
        return Response({'error': 'User not found.'}, status=status.HTTP_404_NOT_FOUND)
    except Group.DoesNotExist:
        return Response({'error': 'Group not found.'}, status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        print(e)

        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['PUT'])
def change_user_group(request,user_id):
    try:
        group_name = request.data['group']
        if not group_name:
            return Response({'error': 'Email and group name are required.'}, status=status.HTTP_400_BAD_REQUEST)
        # Get user by email
        user = User.objects.get(id=user_id)
        # Get or create the group
        group = Group.objects.get(name=group_name)
        # Clear user's current groups and assign the new one
        user.groups.clear()
        user.groups.add(group)
        serializer = UserDataSerializer(user, many=False)
        return Response({'data': serializer}, status=status.HTTP_200_OK)
    except User.DoesNotExist:
        return Response({'error': 'User not found.'}, status=status.HTTP_404_NOT_FOUND)
    except Group.DoesNotExist:
        return Response({'error': 'Group not found.'}, status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        print(e)
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)



@api_view(['DELETE'])
def remove_user_from_admins(request,user_id):
    try:
        user = User.objects.get(id=user_id)
        user.groups.clear()
        return Response({'message': "removed successfully"}, status=status.HTTP_204_NO_CONTENT)
    except User.DoesNotExist:
        return Response({'error': 'User not found.'}, status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
