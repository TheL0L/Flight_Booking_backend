from venv import logger
from rest_framework import generics
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import Flight, Booking
from .serializers import FlightSerializer, BookingSerializer
from datetime import datetime
import json

class FlightList(generics.ListAPIView):
    queryset = Flight.objects.all()
    serializer_class = FlightSerializer

class BookingList(generics.ListAPIView):
    queryset = Booking.objects.all()
    serializer_class = BookingSerializer

def get_locations(request):
    locations = [
        "New York", "London", "Tokyo", "Paris", "Dubai", 
        "Los Angeles", "Singapore", "Toronto", "Mexico City", "Sydney"
    ]
    return JsonResponse({"locations": locations})

@csrf_exempt  # Disable CSRF for simplicity
def search_booking(request):
    if request.method == 'POST':
        # Parse the request body
        data = json.loads(request.body)
        booking_id = data.get('booking_id')

        # Query the Flight model based on the provided filters
        booking = Booking.objects.get(booking_id=booking_id)

        # Prepare the response data
        booking_data = [
            {
                'booking_id': booking.booking_id,
                'flight': {
                    'flight_number': booking.flight.flight_number,
                    'departure': booking.flight.departure,
                    'destination': booking.flight.destination,
                    'departure_time': booking.flight.departure_time.isoformat(),
                    'arrival_time': booking.flight.arrival_time.isoformat(),
                },
                'passenger_first_name': booking.passenger_first_name,
                'passenger_last_name': booking.passenger_last_name,
                'seats': booking.seats,
            }
        ]

        return JsonResponse(booking_data, safe=False)

@csrf_exempt
def search_flights(request):
    if request.method == 'POST':
        # Parse the request body
        data = json.loads(request.body)
        from_location = data.get('departure')
        to_location = data.get('destination')
        departure_time = data.get('departure_time')
        arrival_time = data.get('arrival_time')
        min_seats = data.get('min_seats', 1)

        # Ensure the date-time strings are converted to datetime objects
        try:
            if departure_time:
                departure_time = datetime.fromisoformat(departure_time)
            if arrival_time:
                arrival_time = datetime.fromisoformat(arrival_time)
        except ValueError:
            return JsonResponse({"error": "Invalid date format"}, status=400)

        # Query the Flight model based on the provided filters
        flights = Flight.objects.filter(
            departure=from_location,
            destination=to_location,
            departure_time__gte=departure_time,
        )
        if arrival_time:
            flights = flights.filter(arrival_time__lte=arrival_time)
        flights = flights.filter(total_seats__gte=min_seats)

        # Prepare the response data
        flight_data = [
            {
                'flight_number': flight.flight_number,
                'departure': flight.departure,
                'destination': flight.destination,
                'departure_time': flight.departure_time.isoformat(),
                'arrival_time': flight.arrival_time.isoformat(),
                'available_seats': flight.available_seats(),
            }
            for flight in flights
        ]

        return JsonResponse(flight_data, safe=False)

    return JsonResponse({"error": "Invalid request method"}, status=405)

@csrf_exempt
def book_flight(request):
    """
    Handle flight booking requests with POST data:
    - flight_number: The flight to be booked
    - passenger_first_name: First name of the passenger
    - passenger_last_name: Last name of the passenger
    - seats: Number of seats to book
    """
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            logger.info(f"Received data: {data}")  # Log incoming data
        except json.JSONDecodeError:
            logger.error("Invalid JSON format")
            return JsonResponse({"error": "Invalid JSON format"}, status=400)

        flight_number = data.get('flight_number')
        passenger_first_name = data.get('passenger_first_name')
        passenger_last_name = data.get('passenger_last_name')
        seats = int(data.get('seats'))

        logger.info(f"Parsed fields: flight_number={flight_number}, seats={seats}")

        if not (flight_number and passenger_first_name and passenger_last_name):
            return JsonResponse(
                {"error": "Missing required fields: flight_number, passenger_first_name, passenger_last_name"},
                status=400,
            )

        # Validate seats
        if not isinstance(seats, int):
            return JsonResponse({"error": "Seats must be an integer."}, status=400)
        

        try:
            flight = Flight.objects.get(flight_number=flight_number)
        except Flight.DoesNotExist:
            return JsonResponse({"error": "Flight not found"}, status=404)

        if flight.available_seats() is None:
            return JsonResponse({"error": "Invalid flight data: available seats is None"}, status=400)

        if seats is None:
            return JsonResponse({"error": "Invalid booking data: seats is None"}, status=400)

        if flight.available_seats() < seats:
            return JsonResponse({"error": "Not enough available seats"}, status=400)

        # Reduce available seats
        flight.booked_seats += seats
        flight.save()

        # Create the booking
        booking = Booking.objects.create(
            flight=flight,
            passenger_first_name=passenger_first_name,
            passenger_last_name=passenger_last_name,
            seats=seats,
        )

        return JsonResponse({
            "message": "Booking successful",
            "booking_id": booking.booking_id,
            "flight_number": flight.flight_number,
        })

    return JsonResponse({"error": "Invalid request method"}, status=405)
