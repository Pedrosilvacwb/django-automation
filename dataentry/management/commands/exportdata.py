import csv
from datetime import datetime

from django.core.management.base import BaseCommand, CommandError, CommandParser
from django.db.models import Model

from dataentry.utils import check_csv_errors

# proposed command = python manage.py exportdata model_name


class Command(BaseCommand):
    help = "Export data from the database model ta a CSV file"

    def add_arguments(self, parser: CommandParser) -> None:
        parser.add_argument("model_name", type=str, help="Name of the Model")

    def handle(self, *args, **kwargs):
        model_name = kwargs["model_name"]

        model: Model | None = check_csv_errors(model_name)

        if not model:
            raise CommandError(f'Model "{model_name}" not found')

        data = model.objects.all()

        timestamp = datetime.now().strftime("%Y-%m-%d-%H-%M-%S")
        file_path = f"exported_{model_name}_data_{timestamp}.csv"

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
