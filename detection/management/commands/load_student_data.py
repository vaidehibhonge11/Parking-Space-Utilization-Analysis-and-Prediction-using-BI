import csv
from django.core.management.base import BaseCommand
from detection.models import StudentDetails

class Command(BaseCommand):
    help = 'Load student data from CSV file'

    def add_arguments(self, parser):
        parser.add_argument('csv_file', type=str)

    def handle(self, *args, **kwargs):
        csv_file = kwargs['csv_file']
        with open(csv_file, 'r') as file:
            reader = csv.DictReader(file)
            for row in reader:
                StudentDetails.objects.create(
                    name=row['name'],
                    number_plate=row['number_plate'],
                    year=row['year'],
                    division=row['division'],
                    dept=row['dept'],
                    gender=row['gender']
                )
        self.stdout.write(self.style.SUCCESS('Data loaded successfully'))
