from django.db import models
from apps.customer.models import User
from apps.product.models import Product
# Create your models here.
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

    order_items = models.ManyToManyField(Product)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    status = models.CharField(max_length=2, choices=ORDER_STATUS_CHOICES, default=PENDING)
    delivery_office = models.ForeignKey('DeliveryOffice', on_delete=models.CASCADE)
    cupon = models.ForeignKey('Cupon', null=True, blank=True, on_delete=models.SET_NULL)

    def __str__(self):
        return self.user.username +"-"+ self.status

class DeliveryOffice(models.Model):
    name = models.CharField(max_length=100)
    address = models.TextField()

    def __str__(self):
        return self.user.name

class Cupon(models.Model):
    code = models.CharField(max_length=50)
    percent = models.IntegerField()
    expire = models.DateTimeField()
    count = models.IntegerField(default=-1)

    def __str__(self):
        return self.code

