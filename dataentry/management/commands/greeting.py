from django.core.management.base import BaseCommand, CommandParser


class Command(BaseCommand):
    help = "Prints a custom greeting"

    def add_arguments(self, parser: CommandParser):
        parser.add_argument("name", type=str, help="Specifies user name")
        parser.add_argument("surname", type=str, help="Specifies user surname")

    def handle(self, *args, **kwargs):
        name = kwargs["name"]
        surname = kwargs["surname"]
        greeting = f"Hello Mr {name} {surname}!"
        self.stdout.write(self.style.SUCCESS(greeting))
