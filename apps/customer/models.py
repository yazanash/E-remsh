import datetime
import random
import string

from django.db import models
from django.contrib.auth.models import AbstractUser, Group, Permission


# Create your models here.


class User(AbstractUser):
    email = models.EmailField(unique=True)
    device_token = models.CharField(max_length=255, blank=True, null=True)
    groups = models.ManyToManyField(
        Group,
        related_name='user_groups'  # Unique related_name for your custom model
    )
    user_permissions = models.ManyToManyField(
        Permission,
        related_name='user_permissions'  # Unique related_name for your custom model
    )
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    def save(self, *args, **kwargs):
        if not self.username:
            timestamp = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
            self.username = f"{self.email.split('@')[0]}-{timestamp}"
        if not self.password:
            self.set_password(''.join(random.choices(string.ascii_letters + string.digits, k=8)))
        super().save(*args, **kwargs)


class OTP(models.Model):
    email = models.EmailField(max_length=254)
    otp_code = models.CharField(max_length=6)
    created_at = models.DateTimeField(auto_now_add=True)
    is_valid = models.BooleanField(default=True)

    def __str__(self):
        return f'{self.otp_code} for {self.email}'


class Customer(models.Model):
    Male = 'Male'
    Female = 'Female'

    GENDER_CHOICES = [
        (Male, 'Male'),
        (Female, 'Female'),
    ]
    name = models.CharField(max_length=100)
    gender = models.CharField(max_length=9, choices=GENDER_CHOICES, default=Male)
    phone = models.CharField(max_length=20)
    birthdate = models.CharField(max_length=100)
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')

    def __str__(self):
        return self.name
