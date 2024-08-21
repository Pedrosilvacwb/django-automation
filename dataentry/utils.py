import csv

from django.apps import apps
from django.conf import settings
from django.core.mail import EmailMessage
from django.core.management import CommandError
from django.db import DataError
from django.db.models import Model


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


def send_email_notification(mail_subject, message, to_email):
    try:
        from_email = settings.DEFAULT_FROM_EMAIL
        mail = EmailMessage(mail_subject, message, from_email, to=[to_email])
        mail.send()
    except Exception as e:
        raise e
