from django.core.management.base import BaseCommand
from dataentry.models import Student
# adds data into the database using  the custom command


class Command(BaseCommand):
    help = 'This will insert data into the database.'

    def handle(self, *args, **kwargs):
        # logic goes here
        # creates a new student record that is added to our database table
        # Student.objects.create(roll_no=1001,name='Rosilie',age=20)

        # creates a static set of records using a list with a dictionary
        dataset = [
            {'roll_no': 1002, 'name': 'Yuri', 'age': 22},
            {'roll_no': 1006, 'name': 'Tammy', 'age': 45},
            {'roll_no': 1004, 'name': 'Ziggy', 'age': 13},
            {'roll_no': 1005, 'name': 'Liam', 'age': 10},
        ]

        for data in dataset:
            new_roll_no = data['roll_no']
            # returns T/F by checking if the new record is already existing in our database to avoid duplicates
            existing_record = Student.objects.filter(
                roll_no=new_roll_no).exists()

            if not existing_record:
                # Saves a new unique student record that is added to our database table
                Student.objects.create(
                    roll_no=data['roll_no'], name=data['name'], age=data['age'])
            else:
                self.stdout.write(self.style.WARNING(
                    f'Student with roll_no {new_roll_no} already exists.'))

        self.stdout.write(self.style.SUCCESS(
            'Data inserted successfully.'))
