import random
import string
from django.db import models
from django.core.exceptions import ValidationError

class Flight(models.Model):
    flight_number = models.CharField(max_length=10, unique=True)
    departure = models.CharField(max_length=50)
    destination = models.CharField(max_length=50)
    departure_time = models.DateTimeField()
    arrival_time = models.DateTimeField()
    total_seats = models.PositiveSmallIntegerField(default=100)
    booked_seats = models.PositiveSmallIntegerField(default=0)

    def available_seats(self):
        """Calculate available seats."""
        return self.total_seats - self.booked_seats

    def __str__(self):
        return f"{self.flight_number}: {self.departure} to {self.destination} ({self.available_seats()} seats left)"

class Booking(models.Model):
    booking_id = models.CharField(max_length=20, unique=True)
    flight = models.ForeignKey(Flight, on_delete=models.CASCADE, related_name="bookings")
    passenger_first_name = models.CharField(max_length=50)
    passenger_last_name = models.CharField(max_length=50)
    seats = models.PositiveSmallIntegerField()

    def clean(self):
        """Validate seat availability before saving."""
        if self.seats > self.flight.available_seats():
            raise ValidationError("Not enough seats available on this flight.")

    def save(self, *args, **kwargs):
        """Override save to adjust booked seats on the flight."""
        if self.pk is None:  # This is a new booking
            self.flight.booked_seats += self.seats
            if self.flight.booked_seats > self.flight.total_seats:
                raise ValidationError("This booking exceeds the available seats.")
            self.flight.save()

            # Generate a unique confirmation number
            random_chars = ''.join(random.choices(string.ascii_uppercase + string.digits, k=4))
            self.booking_id = f"{self.flight.flight_number}-{random_chars}"


        else:  # This is an update to an existing booking
            old_booking = Booking.objects.get(pk=self.pk)
            seat_diff = self.seats - old_booking.seats
            if seat_diff > self.flight.available_seats():
                raise ValidationError("This update exceeds the available seats.")
            self.flight.booked_seats += seat_diff
            self.flight.save()

        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.booking_id}: {self.passenger_first_name} {self.passenger_last_name} ({self.seats} seats on flight {self.flight.flight_number})"
