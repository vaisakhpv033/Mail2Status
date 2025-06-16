from celery import shared_task
from django.core.mail import send_mail

from mail2status.genai import get_order_status_from_email
from mail2status.gmail import get_gmail_messages, mark_as_read
from mail2status.settings import DEFAULT_FROM_EMAIL

from .models import Order, OrderStatusLog


@shared_task
def send_email(subject, message, email="vaisakhpv2222@gmail.com"):
    """
    Send an email to the warehouse team.

    Args:
        subject (str): The subject of the email.
        message (str): The body of the email.
        email (str): The recipient's email address. Defaults to warehouse email'
    """
    sender_email = DEFAULT_FROM_EMAIL
    recipient_list = [email]
    send_mail(subject, "", sender_email, recipient_list, html_message=message)
    return f"Email sent to {email} with subject: {subject}"


@shared_task
def update_order_status_from_email():
    print("Checking for unread order-related emails...")

    messages = get_gmail_messages(query="from:vaisakhpv2222@gmail.com is:unread")

    if not messages:
        print("No unread messages found matching the criteria.")
        return

    order_statuses = get_order_status_from_email(messages)

    for message, status_data in zip(messages, order_statuses):
        log = OrderStatusLog.objects.create(
            email_message_id=message.id,
            email_subject=message.subject,
            email_from=message.sender,
            llm_response={
                "order_number": status_data["order_number"],
                "order_status": status_data["order_status"].value,
                "is_valid": status_data["is_valid"],
            },
            is_valid=status_data["is_valid"],
        )

        if status_data["is_valid"]:
            try:
                order = Order.objects.get(order_number=status_data["order_number"])
                log.order = order
                human_readable_status = status_data["order_status"].value
                for db_value, readable in Order.OrderStatus.choices:
                    if readable == human_readable_status:
                        order.status = db_value
                        break
                else:
                    print(f"Invalid status from GenAI: {human_readable_status}")
                order.save()
            except Order.DoesNotExist:
                print(
                    f"No order found with order_number: {status_data['order_number']}"
                )

        log.save()

    mark_as_read(messages)
    print("order status update process completed")
