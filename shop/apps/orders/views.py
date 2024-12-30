from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required
from django.views.generic import ListView
from django.contrib.auth.mixins import LoginRequiredMixin
from .services import OrderService
from .models import Order

@login_required
def create_order(request):
    if request.method == 'POST':
        # Получаем данные корзины из сессии
        cart_items = request.session.get('cart', [])
        if not cart_items:
            return redirect('catalog:product_list')
            
        # Создаем заказ
        order = OrderService.create_order(request.user, cart_items)
        
        # Очищаем корзину
        request.session['cart'] = []
        
        return redirect('orders:history')
    return redirect('catalog:product_list')

def payment_callback(request):
    """
    Обработка callback от платежной системы TON
    """
    order_id = request.POST.get('order_id')
    transaction_id = request.POST.get('transaction_id')
    
    if order_id and transaction_id:
        OrderService.process_payment(order_id, transaction_id)
    
    return JsonResponse({'status': 'ok'})

class OrderHistoryView(LoginRequiredMixin, ListView):
    model = Order
    template_name = 'orders/history.html'
    context_object_name = 'orders'
    
    def get_queryset(self):
        return Order.objects.filter(user=self.request.user).order_by('-created')