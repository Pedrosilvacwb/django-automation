from django.apps import apps
from django.db.models import Model


def search_for_database_model(model_name: str):
    model = None
    for app_config in apps.get_app_configs():
        try:
            model: Model = apps.get_model(app_config.label, model_name)
            break
        except LookupError:
            continue

    return model
