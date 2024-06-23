from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Route, Schedule, Train, Station, Seat, Ticket, Payment, Halt

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'first_name', 'last_name', 'email']

class RouteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Route
        fields = ['route_id', 'starting_station', 'destination_station']

class ScheduleSerializer(serializers.ModelSerializer):

    class Meta:
        model = Schedule
        fields = ['schedule_id', 'arrival_time', 'departure_time', 'route']

class TrainSerializer(serializers.ModelSerializer):
    # schedule = ScheduleSerializer()

    class Meta:
        model = Train
        fields = ['train_no', 'train_name', 'available_seats', 'schedule']

class StationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Station
        fields = ['station_id', 'station_name']

class SeatSerializer(serializers.ModelSerializer):
    # train = TrainSerializer()

    class Meta:
        model = Seat
        fields = ['train', 'coach_no', 'seat_no', 'is_filled']

class TicketSerializer(serializers.ModelSerializer):
    # user = UserSerializer()
    # train = TrainSerializer()

    class Meta:
        model = Ticket
        fields = ['ticket_id', 'ticket_price', 'pnr_no', 'user', 'train']

class PaymentSerializer(serializers.ModelSerializer):
    # ticket = TicketSerializer()

    class Meta:
        model = Payment
        fields = ['payment_id', 'ticket', 'payment_date']
        
class HaltSerializer(serializers.ModelSerializer):
    # station = StationSerializer()
    # train = TrainSerializer()

    class Meta:
        model = Halt
        fields = ['station', 'train', 'arrival_time', 'departure_time']