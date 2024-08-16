import csv
from django.core.management import BaseCommand
# from dataentry.models import Student

# imports all the user installed apps
from django.apps import apps
import datetime

# imports our generate_csv_file funtion from dataentry\utils.py
from dataentry.utils import generate_csv_file
# proposed command = python manage.py exportdata
# proposed command = python manage.py exportdata <modelname>
class Command(BaseCommand):
    help = 'This will export data from any database model  to a CSV file.'

    def add_arguments(self, parser):
        parser.add_argument('model_name', type=str, help='Model Name')

    def handle(self, *args, **kwargs):
        model_name = kwargs['model_name'].capitalize()

        # search through all the installed apps for the model
        target_model = None
        for my_app_config in apps.get_app_configs():
            try:
                # app_config.label is the name we add in the INSTALLED APPS
                # model_name is the the user provided name
                target_model = apps.get_model(my_app_config.label, model_name)
                break  # stops executing once the model is found
            except LookupError:
                pass  # keeps checking to find the desired model

        if not target_model:
            self.stderr.write(f'Model {model_name} could not be found.')
            return

        # fetch data from the database Student
        # students = Student.objects.all()
        # print(students)

        # fetch data from the given desired model name
        data = target_model.objects.all()

        # call a helper function from UTILS.PY
        file_path = generate_csv_file(model_name)

        # We move this block to UTILS.PY  generate_csv_file function
        # ---
        # generate the timestamp of current data and time
        # timestamp = datetime.datetime.now().strftime("%Y-%m-%d-%H-%M-%S")

        # define the csv filename/path as a static filename
        # file_path = f'exported_students_data_{timestamp}.csv'

        # export from any given table as a dynamic name.
        # file_path = f'exported_{model_name}_data_{timestamp}.csv'
        # --

        print(file_path)

        # open the new CSV file and write the data, and close the file after use
        with open(file_path, 'w', newline='') as file:
            writer = csv.writer(file)

            # write the CSV header of Student Model
            # writer.writerow(['Roll No', 'Name', 'Age'])

            # Write the dynamic header row of any desired model
            # print/write the field names of the model we want to export
            writer.writerow(
                [field.name for field in target_model._meta.fields])

            # write the data rows for Student Data
            # for student in students:
            #     writer.writerow([student.roll_no, student.name, student.age])

            # write data rows for any given model
            for dt in data:
                writer.writerow([getattr(dt, field.name)
                                for field in target_model._meta.fields])

        self.stdout.write(self.style.SUCCESS(
            'Data exported as CSV file successfully.'))
