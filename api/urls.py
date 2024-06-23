from django.contrib import admin
from django.urls import path, include
from . import views
from .views import (
    RouteListCreateView, RouteDetailView,
    ScheduleListCreateView, ScheduleDetailView,
    TrainListCreateView, TrainDetailView,
    StationListCreateView, StationDetailView,
    SeatListCreateView, SeatDetailView,
    TicketListCreateView, TicketDetailView,
    PaymentListCreateView, PaymentDetailView,
    HaltListCreateView, HaltDetailView
)
urlpatterns = [
    
    # Auth Views
    path("adminlogin/",views.adminlogin, name="adminlogin"),
    path("login/",views.login, name="login"),
    path("logout/",views.logout, name="logout"),
    path("register/",views.register, name="register"),
    path("user/",views.get_user, name="user"),
    path("test_token/",views.test_token, name="test_token"),
     
    # Model Views
    path('routes/', RouteListCreateView.as_view(), name='route-list-create'),
    path('routes/<int:pk>/', RouteDetailView.as_view(), name='route-detail'),
    path('schedules/', ScheduleListCreateView.as_view(), name='schedule-list-create'),
    path('schedules/<int:pk>/', ScheduleDetailView.as_view(), name='schedule-detail'),
    path('trains/', TrainListCreateView.as_view(), name='train-list-create'),
    path('trains/<int:pk>/', TrainDetailView.as_view(), name='train-detail'),
    path('stations/', StationListCreateView.as_view(), name='station-list-create'),
    path('stations/<int:pk>/', StationDetailView.as_view(), name='station-detail'),
    path('seats/', SeatListCreateView.as_view(), name='seat-list-create'),
    path('seats/<int:pk>/', SeatDetailView.as_view(), name='seat-detail'),
    path('tickets/', TicketListCreateView.as_view(), name='ticket-list-create'),
    path('tickets/<int:pk>/', TicketDetailView.as_view(), name='ticket-detail'),
    path('payments/', PaymentListCreateView.as_view(), name='payment-list-create'),
    path('payments/<int:pk>/', PaymentDetailView.as_view(), name='payment-detail'),
    path('halts/', HaltListCreateView.as_view(), name='halt-list-create'),
    path('halts/<int:pk>/', HaltDetailView.as_view(), name='halt-detail'),
    
    # Custom Views
    path('trains/route/', views.get_trains_by_route, name='get_trains_by_route'),
]