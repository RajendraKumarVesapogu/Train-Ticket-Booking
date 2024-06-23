from django.contrib import admin

from .models import Route, Schedule, Train, Station, Seat, Ticket

admin.site.register(Route)
admin.site.register(Schedule)
admin.site.register(Train)
admin.site.register(Station)
admin.site.register(Seat)
admin.site.register(Ticket)

