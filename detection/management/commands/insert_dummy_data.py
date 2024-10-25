import random
from datetime import datetime, timedelta
from django.core.management.base import BaseCommand
from detection.models import VehicleHourlyStats  # Adjust 'yourapp' to your actual app name

class Command(BaseCommand):
    help = 'Insert dummy data into the VehicleHourlyStats table for training purposes'

    def handle(self, *args, **kwargs):
        self.insert_dummy_data()
    
    def insert_dummy_data(self):
        peak_hours = {
            (8, 9): (15, 25),  # 8-9 AM, rush
            (11, 12): (20, 30),  # 11-12 AM, rush
            (15, 16): (18, 28),  # 3-4 PM, rush
            (17, 18): (20, 35),  # 5-6 PM, rush
        }

        moderate_hours = {
            (9, 11): (5, 15),   # Regular hours before noon
            (12, 15): (7, 12),  # Afternoon regular hours
            (16, 17): (5, 10),  # Pre-evening regular hours
        }

        low_hours = {
            (0, 8): (0, 5),     # Early morning and late night
            (18, 24): (0, 3),   # After 6 PM
        }

        # Insert data for the past 7 days
        start_date = datetime.now() - timedelta(days=7)

        for day in range(7):
            current_date = start_date + timedelta(days=day)
            
            for hour in range(24):
                # Determine vehicle count based on the time of the day
                vehicle_count = 0
                for hour_range, count_range in peak_hours.items():
                    if hour_range[0] <= hour < hour_range[1]:
                        vehicle_count = random.randint(*count_range)
                        break
                for hour_range, count_range in moderate_hours.items():
                    if hour_range[0] <= hour < hour_range[1]:
                        vehicle_count = random.randint(*count_range)
                        break
                for hour_range, count_range in low_hours.items():
                    if hour_range[0] <= hour < hour_range[1]:
                        vehicle_count = random.randint(*count_range)
                        break

                # Insert the dummy data into the VehicleHourlyStats model
                VehicleHourlyStats.objects.create(
                    date=current_date.date(),
                    hour=hour,
                    vehicle_count=vehicle_count
                )
        
        self.stdout.write(self.style.SUCCESS("Dummy data inserted successfully!"))
