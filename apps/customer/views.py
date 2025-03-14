from django.shortcuts import render, get_object_or_404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.core.mail import send_mail
from .models import User, OTP, Customer
from .serializers import UserSerializer, OTPSerializer, CustomerSerializer
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
                    return Response({
                        'message': 'User registered',
                        'refresh': str(refresh),
                        'access': str(refresh.access_token),
                    }, status=status.HTTP_201_CREATED)
                else:
                    return Response({'message': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
            else:
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
            return Response({'message': 'Profile created'}, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def get(self, request):
        user = request.user
        customer = get_object_or_404(Customer, user=user)
        serializer = CustomerSerializer(customer,many=False)
        return Response({"data": serializer.data}, status=status.HTTP_200_OK)


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
            return Response({"refresh": str(new_refresh)}, status=status.HTTP_200_OK)
        except TokenError as e:
            return Response({"message": "Invalid or expired refresh token."}, status=status.HTTP_400_BAD_REQUEST)