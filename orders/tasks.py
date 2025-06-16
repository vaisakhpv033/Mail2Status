from celery import shared_task
from django.core.mail import send_mail
from mail2status.settings import DEFAULT_FROM_EMAIL
from mail2status.genai import get_order_status_from_email
from mail2status.gmail import get_gmail_messages, mark_as_read
from .models import Order, OrderStatusLog


@shared_task
def send_email(subject, message, email="vaisakhpv2222@gmail.com"):
    """
    Send an email to the warehouse team.
    
    Args:
        subject (str): The subject of the email.
        message (str): The body of the email.
        email (str): The recipient's email address. Defaults to '
    """
    sender_email = DEFAULT_FROM_EMAIL
    recipient_list = [email]
    send_mail(subject, message, sender_email, recipient_list)
    return f"Email sent to {email} with subject: {subject}"


@shared_task
def update_order_status_from_email():
    print("Checking for unread order-related emails...")
    messages = get_gmail_messages(query="from:vaisakhpv2222@gmail.com is:unread")
    if not messages:
        print("No unread messages found matching the criteria.")
        return
    
    if messages:
        order_statuses = get_order_status_from_email(messages)
        print("output", order_statuses)
    else:
        print("No unread messages found matching the criteria.")

    mark_as_read(messages)