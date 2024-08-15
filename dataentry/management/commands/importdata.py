from django.core.management.base import BaseCommand, CommandError
# from dataentry.models import Student

# imports all the user installed apps
from django.apps import apps
import csv
from django.db import DataError

# imports our function from dataentry\utils.py
from dataentry.utils import check_csv_error


# proposed command - python manage.py importdata source_file_path target_model_table


class Command(BaseCommand):
    help = 'Imports data from CSV file'

    # accepts a user input like the filename & model_name
    def add_arguments(self, parser):
        parser.add_argument('file_path', type=str, help='Path to the CSV file')
        parser.add_argument('model_name', type=str,
                            help='name of the target model or table name')

    def handle(self, *args, **kwargs):
        # gets the path of the source CSV file and the target model name
        file_path = kwargs['file_path']
        model_name = kwargs['model_name'].capitalize()

        # calls the check_csv_error function in dataentry\utils.property
        target_model = check_csv_error(file_path, model_name)

        with open(file_path, 'r') as file:
            reader = csv.DictReader(file)
            # print(reader)
            # save into our desired target model if there is no error
            for row in reader:
                # adds the row into our database Student table;
                # Student.objects.create(**row)
                # imports the CSV file into the user-provided model
                target_model.objects.create(**row)

        self.stdout.write(self.style.SUCCESS(
            'Data imported from the CSV file successfully.'))
