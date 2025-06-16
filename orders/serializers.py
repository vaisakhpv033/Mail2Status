from rest_framework import serializers

from .models import Order


class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = "__all__"
        read_only_fields = [
            "order_number",
            "created_at",
            "updated_at",
            "status",
            "user",
        ]
