import os
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'flight_booking.settings')
django.setup()

from django.urls import reverse, resolve
from flights.views import (
    FlightList,
    BookingList,
    get_locations,
    search_flights,
    search_booking,
    book_flight,
)

def test_flight_list_url():
    url = reverse("flight-list")
    assert resolve(url).func.view_class == FlightList

def test_booking_list_url():
    url = reverse("booking-list")
    assert resolve(url).func.view_class == BookingList

def test_get_locations_url():
    url = reverse("get_locations")
    assert resolve(url).func == get_locations

def test_search_flights_url():
    url = reverse("search_flights")
    assert resolve(url).func == search_flights

def test_search_booking_url():
    url = reverse("search_booking")
    assert resolve(url).func == search_booking

def test_book_flight_url():
    url = reverse("book_flight")
    assert resolve(url).func == book_flight
