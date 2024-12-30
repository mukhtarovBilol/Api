from decimal import Decimal
from django.conf import settings
import requests


class TONPaymentHandler:
    @staticmethod
    def create_payment(order):
        """
        Создание платежа в TON
        """
        try:
            # Здесь должен быть реальный код для создания платежа в TON
            # Это пример структуры
            payload = {
                'amount': str(order.total_amount),
                'order_id': str(order.id),
                'description': f'Оплата заказа #{order.id}',
                'callback_url': f'{settings.SITE_URL}/api/v1/orders/payment/callback/'
            }

            # Замените на реальный URL API TON
            response = requests.post(
                'https://ton.org/api/payments/create',
                json=payload
            )

            if response.status_code == 200:
                data = response.json()
                return {
                    'payment_url': data['payment_url'],
                    'payment_id': data['payment_id']
                }
            return None
        except Exception as e:
            print(f'Error creating TON payment: {e}')
            return None

    @staticmethod
    def verify_payment(payment_id):
        """
        Проверка статуса платежа
        """
        try:
            # Замените на реальный URL API TON
            response = requests.get(
                f'https://ton.org/api/payments/{payment_id}/status'
            )

            if response.status_code == 200:
                data = response.json()
                return data['status'] == 'completed'
            return False
        except Exception as e:
            print(f'Error verifying TON payment: {e}')
            return False