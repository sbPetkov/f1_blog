from django.db import models
from django.utils.crypto import get_random_string

from f1_blog.merchandise.models import Merchandise


class Order(models.Model):
    PENDING = 'Pending'
    COMPLETED = 'Completed'
    CANCELLED = 'Cancelled'
    STATUS_CHOICES = [
        (PENDING, 'Pending'),
        (COMPLETED, 'Completed'),
        (CANCELLED, 'Cancelled'),
    ]

    order_number = models.CharField(max_length=5, unique=True)
    full_name = models.CharField(max_length=100)
    email = models.EmailField()
    phone_number = models.CharField(max_length=15)
    address = models.TextField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default=PENDING)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        if not self.order_number:
            while True:
                order_number = get_random_string(length=5, allowed_chars='1234567890')
                if not Order.objects.filter(order_number=order_number).exists():
                    self.order_number = order_number
                    break
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Order #{self.order_number}"


class OrderItem(models.Model):
    order = models.ForeignKey(Order, related_name='items', on_delete=models.CASCADE)
    merchandise = models.ForeignKey(Merchandise, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()

    def subtotal(self):
        return self.merchandise.price * self.quantity

    def __str__(self):
        return f"{self.quantity} x {self.merchandise.title} for {self.order}"
