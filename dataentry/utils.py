import csv
import hashlib
import os
import time
from datetime import datetime

from bs4 import BeautifulSoup
from django.apps import apps
from django.conf import settings
from django.core.mail import EmailMessage
from django.core.management import CommandError
from django.db import DataError
from django.db.models import Model

from emails.models import Email, EmailTracking, Sent, Subscriber


def get_all_custom_models() -> list[str]:
    default_models = [
        "ContentType",
        "Session",
        "LogEntry",
        "Group",
        "Permission",
        "Upload",
    ]
    custom_models = []

    for model in apps.get_models():
        if model.__name__ not in default_models:
            custom_models.append(model.__name__)

    return custom_models


def check_csv_errors(file_path: str, model_name: str) -> Model | None:
    model = None

    for app_config in apps.get_app_configs():
        try:
            model: Model = apps.get_model(app_config.label, model_name)
            break
        except LookupError:
            continue

    if not model:
        raise CommandError(f'Model "{model_name}" not found')

    model_fields = [field.name for field in model._meta.fields if field.name != "id"]

    try:
        with open(file_path, "r") as file:
            reader = csv.DictReader(file)
            csv_header = reader.fieldnames

            if csv_header != model_fields:
                raise DataError("CSV file doesn't match with the model fields")
    except Exception as e:
        raise e

    return model


def send_email_notification(
    mail_subject: str,
    message: str,
    to_email: str,
    attachment: str = None,
    email_id: str = None,
):
    try:
        from_email = settings.DEFAULT_FROM_EMAIL

        for email_address in to_email:
            if email_id:
                email = Email.objects.get(pk=email_id)
                subscriber = Subscriber.objects.get(
                    email_list=email.email_list, email_address=email_address
                )
                data_to_hash = f"{email_address}-{str(time.time())}"
                unique_id = hashlib.sha256(data_to_hash.encode()).hexdigest()

                email_tracking = EmailTracking.objects.create(
                    email=email, subscriber=subscriber, unique_id=unique_id
                )

                base_url = settings.BASE_URL
                click_trackin_url = f"{base_url}/emails/track/click/{unique_id}"

                soup = BeautifulSoup(message, "html.parser")

                urls = [a["href"] for a in soup.find_all("a", href=True)]

                if urls:
                    for url in urls:
                        trackin_url = f"{click_trackin_url}?url={url}"
                        message = message.replace(f"{url}", f"{trackin_url}")

                open_tracking_url = f"{base_url}/emails/track/open/{unique_id}"
                open_tracking_img = (
                    f"<img src='{open_tracking_url}' width='1' height='1'>"
                )
                message += open_tracking_img

            mail = EmailMessage(mail_subject, message, from_email, to=[email_address])
            if attachment is not None:
                mail.attach_file(attachment)

            mail.content_subtype = "html"
            mail.send()

        if email_id:
            sent = Sent()
            sent.email = email
            sent.total_sent = email.email_list.count_subscribers()
            sent.save()
    except Exception as e:
        raise e


def get_models_to_context() -> dict:
    models = get_all_custom_models()
    context = {"models": models}
    return context


def generate_csv_file(model_name: str):
    timestamp = datetime.now().strftime("%Y-%m-%d-%H-%M-%S")

    export_dir = "exported"
    file_name = f"exported_{model_name}_data_{timestamp}.csv"

    file_path = os.path.join(settings.MEDIA_ROOT, export_dir, file_name)
    return file_path
