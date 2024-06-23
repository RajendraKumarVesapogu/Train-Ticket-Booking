from django.db import models
from django.contrib.auth.models import User

class Station(models.Model):
    station_id = models.AutoField(primary_key=True)
    station_name = models.CharField(max_length=100)

    def __str__(self):
        return self.station_name

class Route(models.Model):
    route_id = models.AutoField(primary_key=True)
    starting_station = models.ForeignKey(Station, on_delete=models.CASCADE, related_name='starting_routes')
    destination_station = models.ForeignKey(Station, on_delete=models.CASCADE, related_name='destination_routes')

    def __str__(self):
        return f"{self.starting_station} to {self.destination_station}"


class Schedule(models.Model):
    schedule_id = models.AutoField(primary_key=True)
    arrival_time = models.DateTimeField()
    departure_time = models.DateTimeField()
    route = models.ForeignKey(Route, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.route} at {self.arrival_time}"


class Train(models.Model):
    train_no = models.AutoField(primary_key=True)
    train_name = models.CharField(max_length=100)
    available_seats = models.IntegerField()
    route = models.ForeignKey(Route, on_delete=models.CASCADE)
    schedule = models.ForeignKey(Schedule, on_delete=models.CASCADE)

    def __str__(self):
        return self.train_name




class Seat(models.Model):
    train = models.ForeignKey(Train, on_delete=models.CASCADE)
    coach_no = models.CharField(max_length=10)
    seat_no = models.CharField(max_length=10)
    is_filled = models.BooleanField()

    class Meta:
        unique_together = ('train', 'coach_no', 'seat_no')

    def __str__(self):
        return f"Train {self.train}, Coach {self.coach_no}, Seat {self.seat_no}"


class Ticket(models.Model):
    ticket_id = models.AutoField(primary_key=True)
    ticket_price = models.DecimalField(max_digits=10, decimal_places=2)
    pnr_no = models.CharField(max_length=15, unique=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_tickets')
    train = models.ForeignKey(Train, on_delete=models.CASCADE)

    def __str__(self):
        return self.pnr_no


class Payment(models.Model):
    payment_id = models.AutoField(primary_key=True)
    ticket = models.ForeignKey(Ticket, on_delete=models.CASCADE)
    payment_date = models.DateTimeField()

    def __str__(self):
        return f"Payment {self.payment_id} for Ticket {self.ticket}"

class Halt(models.Model):
    station = models.ForeignKey(Station, on_delete=models.CASCADE)
    train = models.ForeignKey(Train, on_delete=models.CASCADE)
    arrival_time = models.DateTimeField()
    departure_time = models.DateTimeField()

    class Meta:
        unique_together = ('station', 'train', 'arrival_time', 'departure_time')

    def __str__(self):
        return f"Train {self.train.train_name} at {self.station.station_name}"