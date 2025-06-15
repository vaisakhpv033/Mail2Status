import os

from celery import Celery


os.environ.setdefault("DJANGO_SETTINGS_MODULE", "mail2status.settings")

celery_app = Celery("mail2status")
celery_app.config_from_object("django.conf:settings", namespace="CELERY")
celery_app.autodiscover_tasks()
