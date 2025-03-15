from django.contrib import admin

# Register your models here.
from .models import *

admin.site.register(Order)
admin.site.register(OrderItems)
admin.site.register(DeliveryOffice)
admin.site.register(Coupon)
