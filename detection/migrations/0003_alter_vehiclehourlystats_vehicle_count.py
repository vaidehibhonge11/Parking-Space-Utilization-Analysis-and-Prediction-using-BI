# Generated by Django 5.0.2 on 2024-10-22 20:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('detection', '0002_vehiclehourlystats'),
    ]

    operations = [
        migrations.AlterField(
            model_name='vehiclehourlystats',
            name='vehicle_count',
            field=models.IntegerField(default=0),
        ),
    ]
