from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.core.mail import send_mail
from .models import User, OTP
from .serializers import UserSerializer, OTPSerializer, CustomerSerializer
from rest_framework_simplejwt.tokens import RefreshToken
import random


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
    def post(self, request):
        serializer = CustomerSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'message': 'Profile created'}, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
