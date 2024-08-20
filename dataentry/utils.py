from django.apps import apps
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


def search_for_database_model(model_name: str) -> Model | None:
    model = None
    for app_config in apps.get_app_configs():
        try:
            model: Model = apps.get_model(app_config.label, model_name)
            break
        except LookupError:
            continue

    return model
