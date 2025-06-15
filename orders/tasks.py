from celery import shared_task
from django.core.mail import send_mail
from mail2status.settings import DEFAULT_FROM_EMAIL


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



