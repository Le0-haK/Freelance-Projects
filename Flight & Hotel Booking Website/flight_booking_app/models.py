from django.db import models
from django.contrib.auth.models import User

class Flight(models.Model):
    flight_number = models.CharField(max_length=20)
    departure_date = models.DateField()
    departure_time = models.TimeField()

    def __str__(self):
        return f"Flight {self.flight_number} - {self.departure_date} {self.departure_time}"

class Booking(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    flight = models.ForeignKey(Flight, on_delete=models.CASCADE)
    seat_number = models.CharField(max_length=60, default=1)

    def __str__(self):
        return f"Booking for customer {self.user.username} on flight {self.flight.flight_number}"

class Hotel(models.Model):
    name = models.CharField(max_length=100)
    address = models.CharField(max_length=200)

    def __str__(self):
        return self.name        

class HotelBooking(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    hotel = models.ForeignKey(Hotel, on_delete=models.CASCADE)
    check_in_date = models.CharField(max_length=100) 
    check_out_date = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.user.username} - {self.hotel.name} ({self.check_in_date} to {self.check_out_date})"        

class HotelReview(models.Model):
    hotel = models.ForeignKey(Hotel, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    rating = models.IntegerField()
    comment = models.TextField()        

class FlightReview(models.Model):
    flight = models.ForeignKey(Flight, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    rating = models.IntegerField()
    comment = models.TextField()    