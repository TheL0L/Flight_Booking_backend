from rest_framework import generics
from .models import Flight
from .serializers import FlightSerializer
from django.http import JsonResponse

class FlightList(generics.ListAPIView):
    queryset = Flight.objects.all()
    serializer_class = FlightSerializer

def get_locations(request):
    locations = [
        "New York", "London", "Tokyo", "Paris", "Dubai", 
        "Los Angeles", "Singapore", "Toronto", "Mexico City", "Sydney"
    ]
    return JsonResponse({"locations": locations})