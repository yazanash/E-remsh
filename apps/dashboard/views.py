from datetime import timedelta

from django.contrib.auth import login, authenticate
from django.contrib.auth.views import LoginView
from django.db.models import Sum, Count
from django.db.models.functions import TruncMonth
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.utils.timezone import now
from django.views.generic.edit import CreateView
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from apps.customer.forms import CustomUserCreationForm
from apps.dashboard.forms import CustomAuthenticationForm, ProductForm
from .decorators import not_logged_user
from .serializers import UserSerializer, CustomAuthenticationFormSerializer
from ..customer.models import Customer
from ..order.models import OrderItems, Order
from ..product.models import Product, Category


# Create your views here.
class UserSignUpAPIView(APIView):
    def post(self, request, *args, **kwargs):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            login(request, user)
            refresh = RefreshToken.for_user(user)
            return Response({
                "message": "User created and logged in successfully",
                "access": str(refresh.access_token),
                "refresh": str(refresh)
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
                return Response({
                    "message": "User logged in successfully",
                    "access": str(refresh.access_token),
                    "refresh": str(refresh)
                }, status=status.HTTP_200_OK)
            return Response({"error": "Invalid email or password"}, status=status.HTTP_401_UNAUTHORIZED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)




