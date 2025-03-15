from django.db import models
from apps.customer.models import User
from apps.product.models import Product


# Create your models here.
class DeliveryOffice(models.Model):
    name = models.CharField(max_length=100)
    address = models.TextField()

    def office(self):
        return f"{self.name}, {self.address}"

    def __str__(self):
        return self.name


class Order(models.Model):
    PENDING = 'P'
    PROCESSING = 'PR'
    SHIPPED = 'S'
    DELIVERED = 'D'
    CANCELED = 'C'

    ORDER_STATUS_CHOICES = [
        (PENDING, 'Pending'),
        (PROCESSING, 'Processing'),
        (SHIPPED, 'Shipped'),
        (DELIVERED, 'Delivered'),
    ]

    user = models.ForeignKey(User, on_delete=models.SET_NULL,null=True)
    status = models.CharField(max_length=2, choices=ORDER_STATUS_CHOICES, default=PENDING)
    delivery_office = models.ForeignKey(DeliveryOffice, null=True,on_delete=models.SET_NULL)
    coupon = models.ForeignKey('Coupon', null=True, blank=True, on_delete=models.SET_NULL)
    total = models.DecimalField(max_digits=10, blank=False, default=0, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user.profile.name + "-" + self.status


class OrderItems(models.Model):
    product = models.ForeignKey(Product, null=True, on_delete=models.SET_NULL)
    order = models.ForeignKey(Order, null=True, on_delete=models.CASCADE, related_name="order_items")
    name = models.CharField(max_length=255, null=False)
    quantity = models.IntegerField(default=1)
    color = models.CharField(max_length=8, null=True, default="000000")
    size = models.CharField(max_length=5, null=True, default="0")
    price = models.DecimalField(max_digits=10, blank=False, decimal_places=2)
    offer = models.DecimalField(max_digits=10, blank=False, default=0, decimal_places=2)
    has_offer = models.BooleanField(default=False)
    percent = models.IntegerField(default=0)
    total = models.DecimalField(max_digits=10, blank=False, default=0, decimal_places=2)
    thumbnail = models.ImageField(upload_to='thumbnails/')


class Coupon(models.Model):
    code = models.CharField(max_length=50)
    percent = models.IntegerField()
    expire = models.DateTimeField()
    count = models.IntegerField(default=-1)

    def __str__(self):
        return self.code
