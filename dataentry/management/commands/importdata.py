from django.core.management.base import BaseCommand, CommandError
# from dataentry.models import Student

# imports all the user installed apps
from django.apps import apps
import csv

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

        # search for the model across all intalled apps
        target_model = None
        for my_app_config in apps.get_app_configs():
            # Try to search for the target model where we will save our imported data
            try:
                # returns the model name  of the app
                target_model = apps.get_model(my_app_config.label, model_name)
                break  # stops search once the model is found
            except LookupError:
                continue  # model is not found, then keep searching in the next app

        # if model is empty/not found
        if not target_model:
            raise CommandError(f'Model "{model_name}" not found in any app.')

        # opens the file for reading and closes it automatically
        with open(file_path, 'r') as file:
            # reads the csv file
            reader = csv.DictReader(file)
            # print(reader)
            for row in reader:
                # adds the row into our database Student table;
                # Student.objects.create(**row)
                # imports the CSV file into the user-provided model
                target_model.objects.create(**row)

        self.stdout.write(self.style.SUCCESS(
            'Data imported from the CSV file successfully.'))
