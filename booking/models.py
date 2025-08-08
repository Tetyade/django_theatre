from django.db import models
from django.contrib.auth.models import User
from decimal import Decimal

class Performance(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    poster = models.ImageField(upload_to='posters')
    troupe = models.TextField(blank=True)  # назва трупи / акторського колективу

    def __str__(self):
        return self.title
    
class PerformanceImage(models.Model):
    performance = models.ForeignKey(Performance, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='performances')


class Hall(models.Model):
    name = models.CharField(max_length=100)
    rows = models.IntegerField()
    seats_per_row = models.IntegerField()

    def __str__(self):
        return self.name

class SeatCategory(models.Model):
    name = models.CharField(max_length=100)
    discount_percent = models.DecimalField(max_digits=5, decimal_places=2, default=0.0)
    color = models.CharField(max_length=7, default="#cccccc")  # для візуального відображення

    def __str__(self):
        return self.name

class Seat(models.Model):
    hall = models.ForeignKey(Hall, on_delete=models.CASCADE, related_name='seats')
    row = models.IntegerField()
    number = models.IntegerField()
    category = models.ForeignKey(SeatCategory, on_delete=models.SET_NULL, null=True, blank=True)

    class Meta:
        unique_together = ('hall', 'row', 'number')
        ordering = ['row', 'number']

    def __str__(self):
        return f"Row {self.row}, Seat {self.number}"

class Session(models.Model):
    performance = models.ForeignKey(Performance, on_delete=models.CASCADE)
    hall = models.ForeignKey(Hall, on_delete=models.CASCADE)
    date = models.DateField()
    time = models.TimeField()
    base_price = models.DecimalField(max_digits=6, decimal_places=2)

    def __str__(self):
        return f"{self.performance.title} — {self.date} {self.time}"
    
    
    def get_price_for_seat(self, seat):
        discount = seat.category.discount_percent if seat.category else Decimal('0')
        return round(self.base_price * (Decimal('1') - discount / Decimal('100')), 2)

class Booking(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    session = models.ForeignKey(Session, on_delete=models.CASCADE)
    seat = models.ForeignKey(Seat, on_delete=models.CASCADE)
    booking_time = models.DateTimeField(auto_now_add=True)
    price_paid = models.DecimalField(max_digits=6, decimal_places=2)

    class Meta:
        unique_together = ('session', 'seat')  # не можна забронювати одне місце двічі!!

    # def get_price_for_seat(self, seat):
    #     discount = seat.category.discount_percent if seat.category else 0
    #     return float(self.base_price) * (1 - discount / 100)
    
    def save(self, *args, **kwargs):
        if not self.price_paid:
            self.price_paid = self.session.get_price_for_seat(self.seat)
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.user.username} — {self.session} — Seat {self.seat}"
