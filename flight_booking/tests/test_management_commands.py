import os
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'flight_booking.settings')
django.setup()

import pytest
from django.core.management import call_command
from flights.models import Flight, Booking


@pytest.mark.django_db
def test_add_bookings_command():
    """Test the add_bookings management command.
    It should add bookings to a flight"""
    # Create a sample flight
    flight = Flight.objects.create(
        flight_number="XY123",
        departure="New York",
        destination="London",
        departure_time="2024-12-01T10:00:00Z",
        arrival_time="2024-12-01T18:00:00Z",
        total_seats=100,
        booked_seats=0,
    )

    # Run the `add_bookings` command
    call_command('add_bookings')

    # Check that bookings have been created for the flight
    flight.refresh_from_db()
    bookings = Booking.objects.filter(flight=flight)
    assert bookings.count() > 0
    assert flight.booked_seats > 0
    for booking in bookings:
        assert booking.seats <= 3  # Ensure no booking exceeds 3 seats

pytest.mark.django_db
def test_populate_flights_command():
    """Test the populate_flights management command.
    It should populate the database with random flights."""
    # Run the `populate_flights` command
    call_command('populate_flights')

    # Check that flights have been created
    flights = Flight.objects.all()
    assert flights.count() == 100  # Ensure 100 flights are created
    for flight in flights:
        assert flight.departure != flight.destination  # Ensure departure and destination are different
        assert flight.total_seats >= 50  # Ensure total seats are within the valid range
        assert flight.total_seats <= 300