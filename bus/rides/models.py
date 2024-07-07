from django.db import models
from django.db.models import F 
from django.contrib.auth.models import User

# Create your models here.

# Modèle représentant un trajet.
class Trip(models.Model):
    origin = models.CharField(max_length=150)
    destination = models.CharField(max_length=150)
    departure_datetime = models.DateTimeField()
    available_seats = models.IntegerField()

    # Retourne une représentation sous forme de chaîne du trajet.
    def __str__(self):
        return f'{self.origin} to {self.destination} on {self.departure_datetime}'

    class Meta:
        verbose_name = 'Trajet'
        verbose_name_plural = 'Trajets'
        unique_together = ('origin', 'destination', 'departure_datetime')

    # Réserve des sièges pour ce trajet s'il y en a suffisamment disponibles.
    def book_seats(self, num_seats):
        if self.available_seats >= num_seats:
            # Utilisation de F() pour éviter les problèmes de concurrence
            self.available_seats = F('available_seats') - num_seats
            self.save()
            return True
        return False

# Modèle représentant une réservation de sièges pour un trajet.
class BooKing(models.Model):
    STATUS_CHOICES = (
        ('confirmed', 'Confirmed'),
        ('pending', 'Pending')
    )
    trip = models.ForeignKey(Trip, on_delete=models.CASCADE, related_name='bookings')
    author = models.ForeignKey(User, null=True, blank=True, on_delete=models.SET_NULL)
    num_seats = models.IntegerField(null=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending')

    # Retourne une représentation sous forme de chaîne de la réservation.
    def __str__(self):
        return f'Booking for {self.num_seats} seats on {self.trip}'

    class Meta:
        verbose_name = 'Reservation'
        verbose_name_plural = 'Reservations'

    
