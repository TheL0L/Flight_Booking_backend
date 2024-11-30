import os
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'flight_booking.settings')
django.setup()

import pytest
from flights.models import Flight, Booking
from django.core.exceptions import ValidationError


@pytest.mark.django_db
def test_flight_available_seats():
    """Test available_seats method and __str__ method of Flight model."""
    flight = Flight.objects.create(
        flight_number="AB123",
        departure="New York",
        destination="London",
        departure_time="2024-12-01T10:00:00Z",
        arrival_time="2024-12-01T18:00:00Z",
        total_seats=100,
        booked_seats=40,
    )
    assert flight.available_seats() == 60
    assert str(flight) == "AB123: New York to London (60 seats left)"

@pytest.mark.django_db
def test_booking_clean():
    """Test clean method of Booking model.
    it raises an error if the number of requested 
    seats exceeds available seats."""
    flight = Flight.objects.create(
        flight_number="CD456",
        departure="Paris",
        destination="Berlin",
        departure_time="2024-12-01T08:00:00Z",
        arrival_time="2024-12-01T10:00:00Z",
        total_seats=50,
        booked_seats=45,
    )
    
    booking = Booking(
        flight=flight,
        passenger_first_name="John",
        passenger_last_name="Doe",
        seats=6,
    )
    with pytest.raises(ValidationError, match="Not enough seats available on this flight."):
        booking.clean()

@pytest.mark.django_db
def test_booking_save():
    """Test save method of Booking model.
    It adjusts the booked seats on the flight and
    generates a unique booking ID."""
    flight = Flight.objects.create(
        flight_number="EF789",
        departure="Tokyo",
        destination="Osaka",
        departure_time="2024-12-02T12:00:00Z",
        arrival_time="2024-12-02T13:30:00Z",
        total_seats=30,
        booked_seats=20,
    )
    booking = Booking.objects.create(
        flight=flight,
        passenger_first_name="Jane",
        passenger_last_name="Smith",
        seats=5,
    )
    
    flight.refresh_from_db()
    assert flight.booked_seats == 25
    assert booking.booking_id.startswith("EF789-")
    assert str(booking) == f"{booking.booking_id}: Jane Smith (5 seats on flight EF789)"