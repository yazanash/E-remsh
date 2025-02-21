from django.contrib import admin

# Register your models here.
from .models import Customer,User

admin.site.register(Customer)
admin.site.register(User)