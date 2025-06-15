from django.contrib import admin
from .models import Order, OrderStatusLog

# Register your models here.
admin.site.register(Order)
admin.site.register(OrderStatusLog)