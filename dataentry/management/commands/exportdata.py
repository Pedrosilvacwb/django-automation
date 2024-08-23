import csv

from django.apps import apps
from django.core.management.base import BaseCommand, CommandError, CommandParser
from django.db.models import Model

from dataentry.utils import generate_csv_file

# proposed command = python manage.py exportdata model_name


class Command(BaseCommand):
    help = "Export data from the database model ta a CSV file"

    def add_arguments(self, parser: CommandParser) -> None:
        parser.add_argument("model_name", type=str, help="Name of the Model")

    def handle(self, *args, **kwargs):
        model_name = kwargs["model_name"]

        model = None

        for app_config in apps.get_app_configs():
            try:
                model: Model = apps.get_model(app_config.label, model_name)
                break
            except LookupError:
                continue

        if not model:
            raise CommandError(f'Model "{model_name}" not found')

        data = model.objects.all()

        file_path = generate_csv_file(model_name)

        with open(file_path, "w", newline="") as file:
            writer = csv.writer(file)

            document_headers = [field.name for field in model._meta.fields]
            writer.writerow(document_headers)

            for record in data:
                data_values = [
                    getattr(record, value.name) for value in model._meta.fields
                ]
                writer.writerow(data_values)

        self.stdout.write(self.style.SUCCESS("Data exported successfully!"))
        return file_path
