from django.db import models

# Airports table
class Airport(models.Model):
    airport_code = models.CharField(max_length=3, primary_key=True)
    airport_name = models.CharField(max_length=100)
    city = models.CharField(max_length=50)
    country = models.CharField(max_length=50)

    def __str__(self):
        return f"{self.airport_name} ({self.airport_code})"

# Flights table
class Flight(models.Model):
    flight_number = models.CharField(max_length=10, unique=True)
    departure_airport = models.ForeignKey(Airport, on_delete=models.CASCADE, related_name="departing_flights")
    arrival_airport = models.ForeignKey(Airport, on_delete=models.CASCADE, related_name="arriving_flights")
    departure_time = models.DateTimeField()
    arrival_time = models.DateTimeField()
    airline = models.CharField(max_length=50)
    total_seats = models.IntegerField()
    available_seats = models.IntegerField()
    price_per_seat = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.flight_number} ({self.departure_airport} -> {self.arrival_airport})"
