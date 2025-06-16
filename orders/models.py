import uuid

from django.db import IntegrityError, models
from django.utils import timezone


class Order(models.Model):
    """
    Represents a customer order containing user and product info, pricing, and delivery address.
    """

    class OrderStatus(models.TextChoices):
        OPEN = "OPEN", "Open"
        CONFIRMED = "CONFIRMED", "Confirmed"
        READY_TO_DISPATCH = "READY_TO_DISPATCH", "Ready to Dispatch"
        IN_TRANSIT = "IN_TRANSIT", "In Transit"

    order_number = models.CharField(
        max_length=100,
        unique=True,
        db_index=True,
        help_text="Unique identifier for the order",
    )
    user = models.PositiveIntegerField(help_text="ID of the customer placing the order")
    product = models.PositiveIntegerField(help_text="ID of the product being ordered")
    quantity = models.PositiveIntegerField(
        default=1, help_text="Quantity of the product in the order"
    )
    price = models.DecimalField(
        max_digits=10, decimal_places=2, help_text="Total price of the order"
    )
    address = models.CharField(
        max_length=255, blank=True, null=True, help_text="Shipping address"
    )
    email = models.EmailField(
        max_length=254, blank=True, null=True, help_text="Email of the customer"
    )
    phone_number = models.CharField(
        max_length=15, blank=True, null=True, help_text="Customer contact number"
    )
    city = models.CharField(
        max_length=100, blank=True, null=True, help_text="City of delivery"
    )
    state = models.CharField(
        max_length=100, blank=True, null=True, help_text="State of delivery"
    )
    postal_code = models.CharField(
        max_length=20, blank=True, null=True, help_text="Postal code for delivery"
    )
    status = models.CharField(
        max_length=30,
        choices=OrderStatus.choices,
        default=OrderStatus.OPEN,
        db_index=True,
        help_text="Current status of the order",
    )
    created_at = models.DateTimeField(
        auto_now_add=True, help_text="Timestamp when the order was created"
    )
    updated_at = models.DateTimeField(
        auto_now=True, help_text="Timestamp when the order was last updated"
    )

    def generate_transaction_no(self):
        """
        Generates a unique order number using timestamp and a UUID fragment.
        """
        unique_id = uuid.uuid4().hex[:12].upper()
        timestamp = timezone.now().strftime("%y%m%d%H%M%S")
        return f"{timestamp}{unique_id}"

    def save(self, *args, **kwargs):
        """
        On creation, generates a unique order number if not already set.
        Retries up to 5 times to avoid collisions.
        """
        if self._state.adding and not self.order_number:
            for _ in range(5):
                self.order_number = self.generate_transaction_no()
                try:
                    super().save(*args, **kwargs)
                    return
                except IntegrityError:
                    continue
            raise IntegrityError("Failed to generate a unique transaction number")
        else:
            super().save(*args, **kwargs)

    def __str__(self):
        return self.order_number

    class Meta:
        verbose_name_plural = "Orders"
        ordering = ["-created_at"]


class OrderStatusLog(models.Model):
    """
    Stores logs of email-based LLM responses to update order status.
    Useful for tracking history, validation, and debugging.
    """

    order = models.ForeignKey(
        Order,
        on_delete=models.SET_NULL,
        related_name="status_logs",
        help_text="Associated order for which the email status was processed",
        blank=True,
        null=True,
    )
    llm_response = models.JSONField(
        blank=True, null=True, help_text="Parsed LLM response derived from the email"
    )
    email_message_id = models.CharField(
        max_length=255,
        unique=True,
        blank=True,
        null=True,
        help_text="Unique Message-ID from the email header",
    )
    email_subject = models.CharField(
        max_length=255, blank=True, null=True, help_text="Subject of the email"
    )
    email_from = models.EmailField(
        max_length=254, blank=True, null=True, help_text="Sender email address"
    )
    received_at = models.DateTimeField(
        auto_now_add=True, help_text="When the email was processed"
    )
    is_valid = models.BooleanField(
        default=False, help_text="True if LLM detected a valid status update"
    )

    def __str__(self):
        return f"Status Log for {(self.order and self.order.order_number) or 'N/A'}"

    class Meta:
        verbose_name_plural = "Order Status Logs"
        ordering = ["-received_at"]
