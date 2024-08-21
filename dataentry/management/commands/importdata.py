# from dataentry.models import Student
import csv

from django.core.management.base import BaseCommand, CommandParser
from django.db.models import Model

from dataentry.utils import check_csv_errors

# Proposed command - python manage.py importdata file_path model_name


class Command(BaseCommand):
    help = "Import data from CSV file"

    def add_arguments(self, parser: CommandParser):
        parser.add_argument("file_path", type=str, help="Path to the CSV file")
        parser.add_argument("model_name", type=str, help="Name of the model")

    def handle(self, *args, **kwargs):
        # logic goes here
        file_path = kwargs["file_path"]
        model_name = kwargs["model_name"].capitalize()

        model: Model | None = check_csv_errors(file_path, model_name)

        with open(file_path, "r") as file:
            reader = csv.DictReader(file)
            for row in reader:
                model.objects.create(**row)
        self.stdout.write(self.style.SUCCESS("Data imported from CSV successfully!"))
