import requests
from django.conf import settings

class TelegramNotifier:
    @staticmethod
    def send_notification(telegram_id, message):
        """
        Отправка уведомления пользователю через Telegram
        """
        if not telegram_id:
            return False
            
        try:
            url = f'https://api.telegram.org/bot{settings.TELEGRAM_BOT_TOKEN}/sendMessage'
            data = {
                'chat_id': telegram_id,
                'text': message,
                'parse_mode': 'HTML'
            }
            response = requests.post(url, data=data)
            return response.status_code == 200
        except Exception as e:
            print(f'Telegram notification error: {e}')
            return False