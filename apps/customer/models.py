from django.db import models
from django.contrib.auth.models import AbstractUser, Group, Permission
# Create your models here.


class User(AbstractUser):
    email = models.EmailField(unique=True)
    groups = models.ManyToManyField(
        Group,
        related_name='custom_user_groups'  # Unique related_name for your custom model
    )
    user_permissions = models.ManyToManyField(
        Permission,
        related_name='custom_user_permissions'  # Unique related_name for your custom model
    )

class OTP(models.Model):
    email = models.EmailField( max_length=254)
    otp_code = models.CharField(max_length=6)
    created_at = models.DateTimeField(auto_now_add=True)
    is_valid = models.BooleanField(default=True)

    def __str__(self):
        return f'{self.otp_code} for {self.user.email}'

class Customer(models.Model):
    name = models.CharField(max_length=100)
    gender = models.CharField(max_length=10)
    phonenumber = models.CharField(max_length=20)
    birthdate = models.DateField()
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')

    def __str__(self):
        return self.name

