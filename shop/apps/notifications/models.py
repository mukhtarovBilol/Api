from django.db import models
from django.conf import settings
from apps.orders.models import Order

class Notification(models.Model):
    TYPE_CHOICES = (
        ('order_status', 'Статус заказа'),
        ('payment', 'Оплата'),
        ('system', 'Системное'),
    )
    
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    order = models.ForeignKey(Order, on_delete=models.CASCADE, null=True, blank=True)
    type = models.CharField(max_length=20, choices=TYPE_CHOICES)
    message = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)
    
    def __str__(self):
        return f'Notification for {self.user.username}'