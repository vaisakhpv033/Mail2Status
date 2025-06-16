from urllib.parse import quote

from django.db.models.signals import post_save
from django.dispatch import receiver

from .models import Order
from .tasks import send_email


@receiver(post_save, sender=Order)
def send_order_email_to_warehouse(sender, instance, created, **kwargs):
    """
    Signal to send an email to the warehouse team when a new order is created.

    Args:
        sender (Model): The model class that sent the signal.
        instance (Order): The instance of the Order that was saved.
        created (bool): Whether a new record was created.
    """
    if created:
        subject = f"New Order Created: {instance.order_number}"
        confirm_subject = f"Order Confirmation for Order Number {instance.order_number}"
        confirm_body = "Your order has been confirmed and we will process it soon."
        mailto_link = f"mailto:communicationsphere033@gmail.com?subject={quote(confirm_subject)}&body={quote(confirm_body)}"

        html_message = f"""
        <html>
            <body style="font-family: Arial, sans-serif; line-height: 1.6;">
                <h2>New Order Notification</h2>
                <p><strong>Order Number:</strong> {instance.order_number}</p>
                <p><strong>Quantity:</strong> {instance.quantity}</p>
                <p><strong>Product:</strong> {instance.product}</p>
                <p><strong>Status:</strong> {instance.status}</p>
                <p><strong>User Email:</strong> {instance.email or "N/A"}</p>
                <p><strong>Phone:</strong> {instance.phone_number or "N/A"}</p>

                <p>Please confirm this order at your earliest convenience.</p>

                <a href="{mailto_link}" style="
                    display: inline-block;
                    padding: 10px 20px;
                    background-color: #28a745;
                    color: white;
                    text-decoration: none;
                    border-radius: 5px;
                    font-weight: bold;
                ">
                    Confirm Order
                </a>
            </body>
        </html>
        """

        send_email.delay(subject, html_message)
