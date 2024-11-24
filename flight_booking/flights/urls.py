from django.urls import path
from .views import FlightList
from .views import get_locations


urlpatterns = [
    path('flights/', FlightList.as_view(), name='flight-list'),
    path("flights/locations/", get_locations, name="get_locations"),
]
