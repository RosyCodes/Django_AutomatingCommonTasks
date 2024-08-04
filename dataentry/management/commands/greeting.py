from django.core.management.base import BaseCommand

# Proposed command = python manage.py greeting Name
# Proposed output = Hello, {Name}! Have a nice day!


class Command(BaseCommand):
    help = "Greets the user."

    # accepts user arguments
    def add_arguments(self, parser):
        # accepts a variable name of type string
        parser.add_argument('name', type=str, help='Specifies user name')

    def handle(self, *args, **kwargs):
        # write the logic
        name = kwargs['name']  # accepts any keyword arguments
        # formats the string
        greeting = f'Hello, {name}! Have a nice day!'
        # self.stdout.write(greeting)

        # shows an error
        # self.stderr.write(greeting)

        # show WARNING message
        # self.stdout.write(self.style.WARNING(greeting))

        # show success message
        self.stdout.write(self.style.SUCCESS(greeting))
