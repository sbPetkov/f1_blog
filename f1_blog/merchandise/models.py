from django.db import models
from django.contrib.auth.models import User


class Category(models.Model):
    name = models.CharField(max_length=100)
    images = models.ImageField(upload_to='merchandise_images/')

    def __str__(self):
        return self.name


class Merchandise(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='merchandise_items')
    images = models.ImageField(upload_to='merchandise_images/')

    def __str__(self):
        return self.title
