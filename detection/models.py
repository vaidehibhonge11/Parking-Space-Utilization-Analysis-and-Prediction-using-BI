from django.db import models

class StudentDetails(models.Model):
    name = models.CharField(max_length=100)
    number_plate = models.CharField(max_length=15, unique=True)
    year = models.CharField(max_length=10)
    division = models.CharField(max_length=1)
    dept = models.CharField(max_length=50)
    gender = models.CharField(max_length=6)

    def __str__(self):
        return self.name


class DetectedVehicle(models.Model):
    number_plate = models.CharField(max_length=15)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.number_plate


class VehicleHourlyStats(models.Model):
    date = models.DateField()
    hour = models.IntegerField()  # Stores the hour (0 to 23)
    vehicle_count = models.IntegerField(default=0)

    def __str__(self):
        return f"{self.date} - {self.hour}: {self.vehicle_count} vehicles"