from decimal import Decimal
from django.db import transaction
from .models import Order, OrderItem
from apps.notifications.services import NotificationService
from utils.ton_payment import TONPaymentProcessor

class OrderService:
    @staticmethod
    @transaction.atomic
    def create_order(user, cart_items):
        """
        Создание заказа из корзины
        """
        total_amount = sum(item['price'] * item['quantity'] for item in cart_items)
        
        order = Order.objects.create(
            user=user,
            total_amount=Decimal(total_amount)
        )
        
        for item in cart_items:
            OrderItem.objects.create(
                order=order,
                product_id=item['product_id'],
                price=item['price'],
                quantity=item['quantity']
            )
            
        # Создаем платеж в TON
        payment = TONPaymentProcessor.create_payment(order.id, total_amount)
        
        # Отправляем уведомление
        NotificationService.send_order_created_notification(order)
        
        return order

    @staticmethod
    def process_payment(order_id, transaction_id):
        """
        Обработка успешной оплаты
        """
        order = Order.objects.get(id=order_id)
        order.status = 'paid'
        order.ton_transaction_id = transaction_id
        order.save()
        
        NotificationService.send_payment_received_notification(order)