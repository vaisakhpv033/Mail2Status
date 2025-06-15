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
        message = f"An order has been created with the following details:\n\n{instance}"
        send_email.delay(subject, message)