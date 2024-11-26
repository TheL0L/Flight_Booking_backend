from django.urls import path
from .views import FlightList, BookingList
from .views import get_locations, search_flights, search_booking


urlpatterns = [
    path('bookings/', BookingList.as_view(), name='booking-list'),
    path('bookings/search/', search_booking, name='search_booking'),
    path('flights/', FlightList.as_view(), name='flight-list'),
    path("flights/locations/", get_locations, name="get_locations"),
    path('flights/search/', search_flights, name='search_flights'),
]
