import json

from django.db import models
from apps.customer.models import User
from apps.customer.models import Customer


# Create your models here.
class Category(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Product(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField()
    colors = models.JSONField(default=list)
    sizes = models.JSONField(default=list)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    offer = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    thumbnail = models.ImageField(upload_to='thumbnails/')
    category = models.ForeignKey(Category, on_delete=models.CASCADE)

    def save(self, *args, **kwargs):
        # Parse colors field if it's a string (from form input)
        if isinstance(self.colors, str):
            self.colors = json.loads(self.colors)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name


class Like(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'product')


class Image(models.Model):
    image_url = models.ImageField(upload_to='thumbnails/')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='images')


class WishList(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'product')
