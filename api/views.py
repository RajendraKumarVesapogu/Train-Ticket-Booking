from django.shortcuts import render
from django.shortcuts import render, get_object_or_404
from rest_framework import generics
from .serializers import UserSerializer, RouteSerializer, ScheduleSerializer, TrainSerializer, StationSerializer, SeatSerializer, TicketSerializer, PaymentSerializer, HaltSerializer
from .models import Route, Schedule, Train, Station, Seat, Ticket, Payment, Halt
from django.contrib.auth.models import User
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.authentication import SessionAuthentication, TokenAuthentication
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.authtoken.models import Token
from django.db import transaction
from rest_framework import generics, permissions
from django.db import connection
from django.utils.crypto import get_random_string


#---------------------------------Home---------------------------------
@api_view(['GET', 'POST', 'PUT', 'DELETE'])
def home(request):
    return Response({'message': 'Api/'})
#---------------------------------User---------------------------------
@api_view(['GET'])
def get_user(request):
    user = get_object_or_404(User, id=request.user_id)
    serializer = UserSerializer(user)
    return Response(serializer.data)
#---------------------------------Login---------------------------------
@api_view(['POST'])
def login(request):
    try:
        user = get_object_or_404(User, email=request.data['email'])
        if user.check_password(request.data['password']):
            token, created = Token.objects.get_or_create(user=user)
            serializer = UserSerializer(user)
            return Response({'token': token.key, 'user': serializer.data})
        else:
            return Response("Invalid credentials", status=status.HTTP_400_BAD_REQUEST)
    except:
        return Response("User not found", status=status.HTTP_404_NOT_FOUND)
#---------------------------------Admin Login---------------------------------
@api_view(['POST'])
def adminlogin(request):
    try:
        user = get_object_or_404(User, email=request.data['email'])
        if user.check_password(request.data['password']) and user.is_superuser:
            token, created = Token.objects.get_or_create(user=user)
            serializer = UserSerializer(user)
            return Response({'token': token.key, 'user': serializer.data})
        else:
            return Response("Invalid credentials", status=status.HTTP_400_BAD_REQUEST)
    except:
        return Response("User not found", status=status.HTTP_404_NOT_FOUND)
#---------------------------------Test Token---------------------------------
@api_view(['GET'])
@authentication_classes([ TokenAuthentication])
@permission_classes([IsAuthenticated])
def test_token(request):
    return Response("passed!")
#---------------------------------Logout---------------------------------
@api_view(['POST', 'GET'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def logout(request):
    try:
        token_key = request.headers.get('Authorization').split(' ')[1]
        token = Token.objects.get(key=token_key)
        token.delete()
        return Response("Logout successful", status=status.HTTP_200_OK)
    except Token.DoesNotExist:
        return Response("Invalid token", status=status.HTTP_401_UNAUTHORIZED)
#---------------------------------Register---------------------------------  
@api_view(['POST'])
def register(request):
    serializer = UserSerializer(data=request.data)
    if serializer.is_valid():
        user = serializer.save()
        user.set_password(request.data['password'])
        user.save()
        token, created = Token.objects.get_or_create(user=user)
        return Response({'token': token.key, 'user': serializer.data}, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


#================================================================================================

#---------------------------------Route---------------------------------

class RouteListCreateView(generics.ListCreateAPIView):
    queryset = Route.objects.all()
    serializer_class = RouteSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

class RouteDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Route.objects.all()
    serializer_class = RouteSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

class ScheduleListCreateView(generics.ListCreateAPIView):
    queryset = Schedule.objects.all()
    serializer_class = ScheduleSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

class ScheduleDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Schedule.objects.all()
    serializer_class = ScheduleSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

class TrainListCreateView(generics.ListCreateAPIView):
    queryset = Train.objects.all()
    serializer_class = TrainSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

class TrainDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Train.objects.all()
    serializer_class = TrainSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

class StationListCreateView(generics.ListCreateAPIView):
    queryset = Station.objects.all()
    serializer_class = StationSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

class StationDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Station.objects.all()
    serializer_class = StationSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

class SeatListCreateView(generics.ListCreateAPIView):
    queryset = Seat.objects.all()
    serializer_class = SeatSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

class SeatDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Seat.objects.all()
    serializer_class = SeatSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

class TicketListCreateView(generics.ListCreateAPIView):
    queryset = Ticket.objects.all()
    serializer_class = TicketSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

class TicketDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Ticket.objects.all()
    serializer_class = TicketSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

class PaymentListCreateView(generics.ListCreateAPIView):
    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

class PaymentDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

class HaltListCreateView(generics.ListCreateAPIView):
    queryset = Halt.objects.all()
    serializer_class = HaltSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

class HaltDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Halt.objects.all()
    serializer_class = HaltSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]


#================================================================================================



@api_view(['POST'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def get_trains_by_route(request):
    starting_station = request.data.get('starting_station')
    destination_station = request.data.get('destination_station')

    if not starting_station or not destination_station:
        return Response({'error': 'Starting station and destination station are required.'}, status=status.HTTP_400_BAD_REQUEST)

    try:
        with connection.cursor() as cursor:
            cursor.execute("""
                SELECT route_id
                FROM api_route
                WHERE starting_station_id = %s AND destination_station_id = %s
            """, [starting_station, destination_station])
            route = cursor.fetchone()

            if not route:
                return Response({'error': 'Route not found.'}, status=status.HTTP_404_NOT_FOUND)
            route_id = route[0]

            cursor.execute("""
                SELECT t.train_no, t.train_name, t.available_seats, t.schedule_id
                FROM api_train t
                
                WHERE t.route_id = %s
            """, [route_id])
            
            rows = cursor.fetchall()
        train_list = []
        for row in rows:
            train_list.append({
                'train_no': row[0],
                'train_name': row[1],
                'available_seats': row[2],
                'schedule': row[3]
            })

        return Response(train_list, status=status.HTTP_200_OK)

    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
    
#--------------------------------------------------------------------------------

@api_view(['GET'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def get_train_details(request, train_no):
    try:
        with connection.cursor() as cursor:
            cursor.execute("""
                SELECT t.train_no, t.train_name, t.available_seats, t.schedule_id, 
                       s.arrival_time, s.departure_time, s.route_id,
                       start_station.station_name AS starting_station, 
                       end_station.station_name AS destination_station
                FROM api_train t
                INNER JOIN api_schedule s ON t.schedule_id = s.schedule_id
                INNER JOIN api_route r ON s.route_id = r.route_id
                INNER JOIN api_station start_station ON r.starting_station_id = start_station.station_id
                INNER JOIN api_station end_station ON r.destination_station_id = end_station.station_id
                WHERE t.train_no = %s
            """, [train_no])
            row = cursor.fetchone()

            if not row:
                return Response({'error': 'Train not found.'}, status=status.HTTP_404_NOT_FOUND)

            train_details = {
                'train_no': row[0],
                'train_name': row[1],
                'available_seats': row[2],
                'schedule': {
                    'schedule_id': row[3],
                    'arrival_time': row[4],
                    'departure_time': row[5],
                    'route': {
                        'route_id': row[6],
                        'starting_station': row[7],
                        'destination_station': row[8],
                    }
                }
            }

        return Response(train_details, status=status.HTTP_200_OK)

    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
#--------------------------------------------------------------------------------

@api_view(['GET'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def get_available_seats(request, train_no):
    try:
        with connection.cursor() as cursor:
            cursor.execute("""
                SELECT t.train_no, t.train_name, t.available_seats, t.schedule_id
                FROM api_train t
                
                WHERE t.train_no = %s
            """, [train_no])
            rows = cursor.fetchall()

            if not rows:
                return Response({'error': 'No available seats found for this train.'}, status=status.HTTP_404_NOT_FOUND)

            available_seats = [
                {
                    'available_seats': row[2],
                } for row in rows
            ]

        return Response(available_seats, status=status.HTTP_200_OK)

    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
#--------------------------------------------------------------------------------

@api_view(['POST'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def book_ticket(request, train_no):
    try:
        with transaction.atomic():
            # Retrieve the train
            train = Train.objects.select_for_update().get(train_no=train_no)

            if train.available_seats <= 0:
                return Response({'error': 'No available seats.'}, status=status.HTTP_400_BAD_REQUEST)

            # Find an available seat
            available_seat = Seat.objects.select_for_update().filter(train=train, is_filled=False).first()
            if not available_seat:
                return Response({'error': 'No available seats.'}, status=status.HTTP_400_BAD_REQUEST)

            # Log the available seat details
            print(f"Available Seat: {available_seat.coach_no}-{available_seat.seat_no}")

            # Mark the seat as filled
            available_seat.is_filled = True
            available_seat.save()

            # Create the ticket
            pnr_no = get_random_string(15).upper()  # Generate a random PNR number
            ticket_price = request.data.get('ticket_price', 0.0)  # Assume ticket_price is passed in the request body

            ticket = Ticket.objects.create(
                ticket_price=ticket_price,
                pnr_no=pnr_no,
                user=request.user,
                train=train
            )

            # Decrement the available seats
            train.available_seats -= 1
            train.save()

            return Response({
                'pnr_no': ticket.pnr_no,
                'ticket_price': ticket.ticket_price,
                'train': {
                    'train_no': train.train_no,
                    'train_name': train.train_name
                },
                'seat': {
                    'seat_no': available_seat.seat_no,
                    'coach_no': available_seat.coach_no
                }
            }, status=status.HTTP_201_CREATED)

    except Train.DoesNotExist:
        return Response({'error': 'Train not found.'}, status=status.HTTP_404_NOT_FOUND)
    # except IntegrityError:
    #     return Response({'error': 'Error occurred during booking. Please try again.'}, status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
    
#--------------------------------------------------------------------------------
@api_view(['POST'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def cancel_ticket(request, train_no, ticket_id):
    try:
        # Get the ticket to be canceled
        ticket = Ticket.objects.get(pk=ticket_id, train__train_no=train_no, user=request.user)

        # Get the train associated with the ticket
        train = ticket.train

        # Delete the ticket
        ticket.delete()

        # Increment the available seats in the train
        train.available_seats += 1
        train.save()

        return Response({'message': 'Ticket canceled successfully.'}, status=status.HTTP_200_OK)

    except Ticket.DoesNotExist:
        return Response({'error': 'Ticket not found.'}, status=status.HTTP_404_NOT_FOUND)

    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
#--------------------------------------------------------------------------------
@api_view(['GET'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def list_user_tickets(request):
    try:
        # Get all tickets belonging to the authenticated user
        tickets = Ticket.objects.filter(user=request.user)

        # Serialize the tickets
        serializer = TicketSerializer(tickets, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)

    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
#--------------------------------------------------------------------------------
@api_view(['GET'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def get_user_ticket_details(request, train_no, ticket_id):
    try:
        # Get the ticket belonging to the authenticated user and the specified train
        ticket = Ticket.objects.get(pk=ticket_id, train__train_no=train_no, user=request.user)

        # Serialize the ticket
        serializer = TicketSerializer(ticket)

        return Response(serializer.data, status=status.HTTP_200_OK)

    except Ticket.DoesNotExist:
        return Response({'error': 'Ticket not found.'}, status=status.HTTP_404_NOT_FOUND)

    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
#--------------------------------------------------------------------------------

from datetime import datetime
from django.utils import timezone

@api_view(['POST'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def make_payment(request, train_no, ticket_id):
    try:
        # Get the ticket to be paid
        ticket = Ticket.objects.get(pk=ticket_id, train__train_no=train_no, user=request.user)

        # Check if the ticket is already paid
        if Payment.objects.filter(ticket=ticket).exists():
            return Response({'error': 'Ticket already paid.'}, status=status.HTTP_400_BAD_REQUEST)

        # Create a payment record
        payment = Payment.objects.create(ticket=ticket, payment_date=timezone.now())

        return Response({'message': 'Payment successful.', 'payment_id': payment.payment_id, 'ticket_id' : ticket.ticket_id}, status=status.HTTP_200_OK)

    except Ticket.DoesNotExist:
        return Response({'error': 'Ticket not found.'}, status=status.HTTP_404_NOT_FOUND)

    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
#--------------------------------------------------------------------------------

@api_view(['GET'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def get_payment_details(request, train_no, ticket_id):
    try:
        # Get the payment details for the specified ticket in the specified train
        payment = Payment.objects.get(ticket_id=ticket_id, ticket__train__train_no=train_no, ticket__user=request.user)

        # Serialize the payment details
        serializer = PaymentSerializer(payment)

        return Response(serializer.data, status=status.HTTP_200_OK)

    except Payment.DoesNotExist:
        return Response({'error': 'Payment details not found.'}, status=status.HTTP_404_NOT_FOUND)

    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
#--------------------------------------------------------------------------------

@api_view(['GET'])
def list_halts_for_train(request, train_no):
    try:
        halts = Halt.objects.filter(train__train_no=train_no)
        serializer = HaltSerializer(halts, many=True)
        return Response(serializer.data)
    except Halt.DoesNotExist:
        return Response({'error': 'Halts not found for the specified train.'}, status=status.HTTP_404_NOT_FOUND)
#--------------------------------------------------------------------------------
@api_view(['GET'])
def list_trains_for_station(request, station_id):
    try:
        # Get all halts for the specified station
        halts = Halt.objects.filter(station_id=station_id)
        
        # Extract train IDs from halts
        train_ids = [halt.train_id for halt in halts]
        
        # Get all trains that have halts at the specified station
        trains = Train.objects.filter(train_no__in=train_ids)
        
        # Serialize the data
        data = []
        for train in trains:
            halt = halts.filter(train_id=train.train_no).first()
            train_data = {
                'train_no': train.train_no,
                'train_name': train.train_name,
                'available_seats': train.available_seats,
                'arrival_time': halt.arrival_time,
                'departure_time': halt.departure_time,
            }
            data.append(train_data)
        
        return Response(data)
    except Halt.DoesNotExist:
        return Response({'error': 'No halts found for the specified station.'}, status=status.HTTP_404_NOT_FOUND)






    