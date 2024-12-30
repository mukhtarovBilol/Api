from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import Order
from .serializers import OrderSerializer
from .services import OrderService


class OrderViewSet(viewsets.ModelViewSet):
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Order.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        cart_items = self.request.data.get('cart_items', [])
        order = OrderService.create_order(self.request.user, cart_items)
        return order

    @action(detail=True, methods=['post'])
    def pay(self, request, pk=None):
        order = self.get_object()
        # Здесь будет логика оплаты
        return Response({'status': 'payment initiated'})