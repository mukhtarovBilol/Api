from .models import Notification
from utils.telegram import TelegramNotifier

class NotificationService:
    @staticmethod
    def create_notification(user, type_name, message, order=None):
        """
        Создание уведомления
        """
        notification = Notification.objects.create(
            user=user,
            type=type_name,
            message=message,
            order=order
        )
        
        # Отправляем в Telegram, если у пользователя есть Telegram ID
        if user.profile.telegram_id:
            TelegramNotifier.send_notification(
                user.profile.telegram_id,
                message
            )
        
        return notification

    @staticmethod
    def send_order_created_notification(order):
        """
        Уведомление о создании заказа
        """
        message = f'Заказ #{order.id} создан. Ожидает оплаты.'
        return NotificationService.create_notification(
            order.user,
            'order_status',
            message,
            order
        )

    @staticmethod
    def send_payment_received_notification(order):
        """
        Уведомление об успешной оплате
        """
        message = f'Оплата заказа #{order.id} получена. Заказ передан в обработку.'
        return NotificationService.create_notification(
            order.user,
            'payment',
            message,
            order
        )