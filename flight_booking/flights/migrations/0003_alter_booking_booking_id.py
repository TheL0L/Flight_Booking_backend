# Generated by Django 5.1.3 on 2024-11-29 22:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('flights', '0002_flight_booked_seats_flight_total_seats_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='booking',
            name='booking_id',
            field=models.CharField(max_length=20, unique=True),
        ),
    ]
