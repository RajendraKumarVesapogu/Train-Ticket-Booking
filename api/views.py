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
                INNER JOIN api_schedule s ON t.schedule_id = s.schedule_id
                WHERE s.route_id = %s
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