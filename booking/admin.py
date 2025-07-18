from django.contrib import admin
from booking.models import Performance, PerformanceImage, Hall, SeatCategory, Seat, Session, Booking

admin.site.register(Performance)
admin.site.register(PerformanceImage)
admin.site.register(Hall)
admin.site.register(SeatCategory)
admin.site.register(Seat)
admin.site.register(Session)
admin.site.register(Booking)
