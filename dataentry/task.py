import time

from django.conf import settings
from django.core.management import call_command

from awd_main.celery import app

from .utils import send_email_notification


@app.task
def celery_test_task():
    time.sleep(10)

    mail_subject = "Test subject"
    message = "This is a test email"
    to_email = settings.DEFAULT_TO_EMAIL

    send_email_notification(mail_subject, message, to_email)
    return "Email sent successfully"


@app.task
def import_data_task(file_path: str, model_name: str):
    try:
        call_command("importdata", file_path, model_name)

    except Exception as e:
        raise e

    mail_subject = "Import Data Completed"
    message = "Your data import has been completed"
    to_email = settings.DEFAULT_TO_EMAIL

    send_email_notification(mail_subject, message, to_email)
    return "Data returned successfully!"
