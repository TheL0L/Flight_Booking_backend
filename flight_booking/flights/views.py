from rest_framework import generics
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import Flight, Booking
from .serializers import FlightSerializer, BookingSerializer
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
