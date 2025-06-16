import os
from celery import Celery


os.environ.setdefault("DJANGO_SETTINGS_MODULE", "mail2status.settings")

celery_app = Celery("mail2status")
celery_app.config_from_object("django.conf:settings", namespace="CELERY")
celery_app.autodiscover_tasks()


@celery_app.on_after_configure.connect
def setup_periodic_tasks(sender: Celery, **kwargs):
    sender.add_periodic_task(
        30.0,
        celery_app.signature('orders.tasks.update_order_status_from_email'),
        name='add 30'
    )


# @celery_app.task
# def test():
#     """
#     A simple test task to verify Celery is working.
#     """
#     print("Test task executed successfully.")
#     return "Test task completed."