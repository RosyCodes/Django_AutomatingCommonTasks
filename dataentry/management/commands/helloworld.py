# imports the BaseCommands for custom commands
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = "Prints Hello World"

    # entry point
    def handle(self, *args, **kwargs):
        # we write the logic
        self.stdout.write('Hello World')
