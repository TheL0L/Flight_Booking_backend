from django.core.management.base import BaseCommand
from flights.models import Flight
from datetime import datetime, timedelta
import random


class Command(BaseCommand):
    help = "Populates the database with random flight data"

    def generate_random_flight(self):
        # Define a list of possible locations
        locations = [
            "New York", "London", "Tokyo", "Paris", "Dubai", 
            "Los Angeles", "Singapore", "Toronto", "Mexico City", "Sydney"
        ]

        # Ensure departure and destination are different
        departure, destination = random.sample(locations, 2)

        # Generate random times
        departure_time = datetime.now() + timedelta(
            days=random.randint(1, 30),
            hours=random.randint(0, 23),
            minutes=random.randint(0, 59)
        )
        # Add 2 to 12 hours for the arrival time
        arrival_time = departure_time + timedelta(hours=random.randint(2, 12))

        # Generate a random flight number and ensure it's unique
        while True:
            flight_number = f"{random.choice('ABCDEFGHIJKLMNOPQRSTUVWXYZ')}{random.randint(100, 999)}"
            if not Flight.objects.filter(flight_number=flight_number).exists():
                break

        # Generate random total seats (between 50 and 300)
        total_seats = random.randint(50, 300)

        return {
            "flight_number": flight_number,
            "departure": departure,
            "destination": destination,
            "departure_time": departure_time,
            "arrival_time": arrival_time,
            "total_seats": total_seats,
        }

    def handle(self, *args, **kwargs):
        Flight.objects.all().delete()  # Clear existing data
        self.stdout.write("Clearing existing flight data...")
        Flight.objects.all().delete()

        # Number of flights to generate
        num_flights = 100

        # Create random flights
        self.stdout.write(f"Generating {num_flights} random flights...")
        for _ in range(num_flights):
            flight_data = self.generate_random_flight()
            Flight.objects.create(**flight_data)

        self.stdout.write(self.style.SUCCESS(f"Successfully populated {num_flights} flights!"))
