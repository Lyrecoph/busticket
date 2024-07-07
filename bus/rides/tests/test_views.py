from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from django.contrib.auth.models import User
from rides.models import Trip, BooKing

class TripListCreateViewTests(APITestCase):
    fixtures = ['initial_data.json']

    def test_list_trips_with_available_seats(self):
        url = reverse('trip-list-create')
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 5)

    def test_create_trip(self):
        url = reverse('trip-list-create')
        data = {
            "origin": "Abidjan",
            "destination": "Daloa",
            "departure_datetime": "2024-10-01T08:00:00Z",
            "available_seats": 20
        }

        # Créer un utilisateur et l'authentifier
        user = User.objects.create_user(username='testuser', password='testpassword')
        self.client.force_authenticate(user=user)

        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Trip.objects.count(), 7)  # Vérifie que le nombre de trajets a augmenté

class BookingListCreateViewTests(APITestCase):
    fixtures = ['initial_data.json']

    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpassword')

    def test_list_bookings(self):
        url = reverse('booking-list-create')
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # Total des réservations dans initial_data.json
        self.assertEqual(len(response.data), 6)  

    # Vérifie la liste des réservations filtrées par `trip_id`
    def test_list_bookings_filtered_by_trip_id(self):
        url = reverse('booking-list-create')
        response = self.client.get(url, {'trip_id': 1}, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)

    # Vérifier la création d'une réservation par un utilisateur authentifié 
    def test_create_booking_authenticated_user(self):
        url = reverse('booking-list-create')
        data = {
            "trip_id": 1,
            "num_seats": 2
        }
        
        # Authentifier l'utilisateur
        self.client.force_authenticate(user=self.user)

        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        # Vérifier que la réservation a été créée avec succès
        booking = BooKing.objects.get(id=response.data['id'])
        self.assertEqual(booking.num_seats, 2)
        self.assertEqual(booking.status, 'pending')

        # Vérifier que les places disponibles du trajet ont diminué correctement
        trip = Trip.objects.get(id=1)
        self.assertEqual(trip.available_seats, 13)  # Déduction de 15 places initiales moins 2 réservées


    # Vérifie la création d'une réservation par un utilisateur anonyme
    def test_create_booking_anonymous_user(self):
        self.client.logout()
        url = reverse('booking-list-create')
        data = {
            "trip_id": 1,
            "num_seats": 2
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        booking = BooKing.objects.get(id=response.data['id'])
        self.assertEqual(booking.num_seats, 2)
        # Vérifie que le statut par défaut est "pending"
        self.assertEqual(booking.status, 'pending')  
        trip = Trip.objects.get(id=1)
        # Vérifie que les places disponibles ont diminué(15 - 3 - 2 places réservées)
        self.assertEqual(trip.available_seats, 13)  

    # Vérifie l'échec de la création d'une réservation lorsque le nombre de sièges 
	# disponibles est insuffisant
    def test_create_booking_insufficient_seats(self):
        url = reverse('booking-list-create')
        data = {
            "trip": 6,  # Ce trajet a 0 places disponibles
            "num_seats": 1
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    # Vérifie l'échec de la création d'une réservation avec un nombre de sièges négatif
    def test_create_booking_negative_seats(self):
        url = reverse('booking-list-create')
        data = {
            "trip": 1,
            "num_seats": -1
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    # Vérifie l'échec de la création d'une réservation avec zéro siège
    def test_create_booking_zero_seats(self):
        url = reverse('booking-list-create')
        data = {
            "trip": 1,
            "num_seats": 0
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

class TripRevenueViewTests(APITestCase):
    fixtures = ['initial_data.json']

    def test_get_trip_revenue(self):
        trip_id = 1
        url = reverse('trip-revenue', args=[trip_id])
        # Créer un utilisateur et l'authentifier
        user = User.objects.create_user(username='testuser', password='testpassword')
        self.client.force_authenticate(user=user)
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('revenue', response.data)
