import os
import random
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'flight_booking.settings')
django.setup()

import pytest
from flights.models import Flight, Booking
from flights.serializers import FlightSerializer, BookingSerializer
from datetime import datetime, timedelta

def generate_unique_flight_id():
    while True:
        unique_id = f"{random.choice('ABCDEFGHIJKLMNOPQRSTUVWXYZ')}{random.randint(100, 999)}"
        if not Flight.objects.filter(flight_number=unique_id).exists():
            break
    return unique_id

@pytest.mark.django_db
def test_flight_serializer():
    unique_id = generate_unique_flight_id()
    # Create a flight instance
    flight = Flight.objects.create(
        flight_number=unique_id,
        departure="New York",
        destination="London",
        departure_time="2024-12-01T10:00:00Z",
        arrival_time="2024-12-01T18:00:00Z",
        total_seats=150,
        booked_seats=30,
    )

    # Serialize the flight instance
    serializer = FlightSerializer(flight)
    data = serializer.data

    #delete the object we created
    flight.delete()
    
    # Validate serialized data
    assert data["flight_number"] == unique_id
    assert data["departure"] == "New York"
    assert data["destination"] == "London"
    assert data["total_seats"] == 150
    assert data["booked_seats"] == 30
    

@pytest.mark.django_db
def test_flight_serializer_validation():
    # Test validation with invalid data (e.g., missing required fields)
    invalid_data = {
        "flight_number": "XY789",  # Missing other required fields
    }
    serializer = FlightSerializer(data=invalid_data)
    assert not serializer.is_valid()
    assert "departure" in serializer.errors
    assert "destination" in serializer.errors

@pytest.mark.django_db
def test_booking_serializer():
    unique_id = generate_unique_flight_id()

    # Create a flight instance
    flight = Flight.objects.create(
        flight_number=unique_id,
        departure="Paris",
        destination="Berlin",
        departure_time="2024-12-01T08:00:00Z",
        arrival_time="2024-12-01T12:00:00Z",
        total_seats=100,
        booked_seats=20,
    )

    # Create a booking instance
    booking = Booking.objects.create(
        flight=flight,
        passenger_first_name="John",
        passenger_last_name="Doe",
        seats=2,
    )

    # Serialize the booking instance
    serializer = BookingSerializer(booking)
    data = serializer.data

    flight_id:int = flight.id
    #delete the objects we created
    flight.delete()
    booking.delete()

    # Validate serialized data
    assert data["flight"] == flight_id
    assert data["passenger_first_name"] == "John"
    assert data["passenger_last_name"] == "Doe"
    assert data["seats"] == 2
