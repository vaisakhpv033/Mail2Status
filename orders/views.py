from rest_framework.generics import CreateAPIView

from .models import Order
from .serializers import OrderSerializer


class CreateOrderView(CreateAPIView):
    """
    View to create a new order.
    """

    serializer_class = OrderSerializer
    queryset = Order.objects.all()

    def perform_create(self, serializer):
        serializer.save(user=1)
