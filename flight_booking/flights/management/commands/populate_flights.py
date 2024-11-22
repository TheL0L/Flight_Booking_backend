from django.core.management.base import BaseCommand
from flights.models import Flight
from datetime import datetime, timedelta

class Command(BaseCommand):
    help = "Populates the database with sample flight data"

    def handle(self, *args, **kwargs):
        Flight.objects.all().delete()  # Clear existing data
        flights = [
            {
                "flight_number": "AB123",
                "departure": "New York",
                "destination": "London",
                "departure_time": datetime.now() + timedelta(days=1),
                "arrival_time": datetime.now() + timedelta(days=1, hours=6),
            },
            {
                "flight_number": "CD456",
                "departure": "Los Angeles",
                "destination": "Tokyo",
                "departure_time": datetime.now() + timedelta(days=2),
                "arrival_time": datetime.now() + timedelta(days=2, hours=11),
            },
            {
                "flight_number": "EF789",
                "departure": "Paris",
                "destination": "Dubai",
                "departure_time": datetime.now() + timedelta(days=3),
                "arrival_time": datetime.now() + timedelta(days=3, hours=7),
            },
        ]

        for flight_data in flights:
            Flight.objects.create(**flight_data)

        self.stdout.write(self.style.SUCCESS("Successfully populated flights!"))
