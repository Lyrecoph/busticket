from django.contrib.auth.models import User
from django.test import TestCase

from rides.models import Trip, BooKing

class TripModelTests(TestCase):
    fixtures = ['initial_data.json']

    # Vérifie la création d'un trajet
    def test_create_trip(self):
        trip = Trip.objects.create(
            origin='Abuja',
            destination='Cotonou',
            departure_datetime='2024-12-25T10:00:00Z',
            available_seats=50
        )
        # Suppose 6 voyages dans initial_data.json + 1 nouveau voyage
        self.assertEqual(Trip.objects.count(), 7)  

    # Vérifie la représentation en chaîne de caractères d'un trajet
    def test_trip_str(self):
        trip = Trip.objects.get(id=1)
        expected_str = f'{trip.origin} to {trip.destination} on {trip.departure_datetime}'
        self.assertEqual(str(trip), expected_str)

    # Vérifie la représentation en chaîne de caractères d'une réservation
    def test_booking_str(self):
        booking = BooKing.objects.get(id=1)
        expected_str = f'Booking for {booking.num_seats} seats on {booking.trip}'
        self.assertEqual(str(booking), expected_str)

    # Vérifie la création d'une réservation
    def test_create_booking(self):
        trip = Trip.objects.get(id=1)
        user = User.objects.create_user(username='testuser2', password='password')
        booking = BooKing.objects.create(
            trip=trip,
            author=user,
            num_seats=2,
            status='pending'
        )
        # Suppose 6 réservations dans initial_data.json + 1 nouvelle réservation
        self.assertEqual(BooKing.objects.count(), 7)  

    # Vérifie la réservation de sièges avec succès
    def test_book_seats_success(self):
        trip = Trip.objects.get(id=1)
        initial_seats = trip.available_seats
        success = trip.book_seats(3)
        trip.refresh_from_db()
        self.assertTrue(success)
        self.assertEqual(trip.available_seats, initial_seats - 3)

    # Vérifie l'échec de la réservation de sièges lorsque le nombre de sièges 
    # disponibles est insuffisant
    def test_book_seats_failure(self):
        trip = Trip.objects.get(id=1)
        initial_seats = trip.available_seats
        success = trip.book_seats(initial_seats + 1)
        trip.refresh_from_db()
        self.assertFalse(success)
        self.assertEqual(trip.available_seats, initial_seats)

    # Vérifie la contrainte d'unicité pour la création de trajets avec la même origine, destination 
	   et horaire de départ
    def test_unique_together_constraint(self):
        trip1 = Trip.objects.create(
            origin='Abuja',
            destination='Cotonou',
            departure_datetime='2024-12-25T10:00:00Z',
            available_seats=50
        )
        # Vous pouvez spécifier l'exception exacte si vous le souhaitez
        with self.assertRaises(Exception):  
            Trip.objects.create(
                origin='Abuja',
                destination='Cotonou',
                departure_datetime='2024-12-25T10:00:00Z',
                available_seats=50
            )
