from django.core.management.base import BaseCommand
from flights.models import Flight, Booking
import random
from django.core.exceptions import ValidationError
from django.db.utils import IntegrityError


class Command(BaseCommand):
    help = "Populates the database with random bookings for existing flights, leaving some seats unbooked."

    def generate_random_passenger(self):
        """Generate random passenger details."""
        first_names = ["John", "Jane", "Alice", "Bob", "Charlie", "Emily", "Frank", "Grace", "Hannah", "Ivy"]
        last_names = ["Smith", "Johnson", "Williams", "Brown", "Jones", "Garcia", "Miller", "Davis", "Rodriguez", "Martinez"]
        return {
            "passenger_first_name": random.choice(first_names),
            "passenger_last_name": random.choice(last_names),
        }

    def handle(self, *args, **kwargs):
        # Clear existing bookings before starting
        self.stdout.write("Clearing existing bookings...")
        Booking.objects.all().delete()

        # Fetch all flights
        flights = Flight.objects.all()
        if not flights.exists():
            self.stdout.write(self.style.ERROR("No flights available. Populate flights first."))
            return

        # Percentage of capacity to fill bookings per flight
        capacity = 0.7

        self.stdout.write(f"Generating bookings to reach {capacity * 100}% capacity...")

        for i, flight in enumerate(flights):
            seats_to_fill = int(flight.available_seats() * capacity)
            self.stdout.write(f"Flight {i + 1}/{len(flights)} (generating {seats_to_fill} bookings)...")

            # Track booked seats for this flight
            seats_booked = 0

            while seats_booked < seats_to_fill:
                # Generate random passenger details
                passenger_data = self.generate_random_passenger()

                # Randomly select a number of seats to book (1-3)
                seats_to_book = random.randint(1, min(3, seats_to_fill - seats_booked))

                # Generate a random booking_id and ensure it's unique
                booking_id = random.randint(10000, 99999)
                while Booking.objects.filter(booking_id=booking_id).exists():
                    booking_id = random.randint(10000, 99999)  # Retry until unique

                # Create the booking
                try:
                    Booking.objects.create(
                        booking_id=booking_id,
                        flight=flight,
                        seats=seats_to_book,
                        **passenger_data,
                    )
                    seats_booked += seats_to_book
                except IntegrityError as e:
                    # Handle integrity errors if the booking can't be created
                    self.stderr.write(f"Error creating booking for flight {flight.flight_number}: {e}")
                    continue  # Skip invalid bookings

        self.stdout.write(self.style.SUCCESS("Database successfully populated with bookings!"))
