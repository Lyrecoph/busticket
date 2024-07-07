from django.contrib.auth.models import User
from django.db import transaction
from django.shortcuts import get_object_or_404

from rest_framework import authentication, generics, permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView

from .permissions import IsAuthenticatedOrCreateOnly
from  rides.models import Trip, BooKing
from .serializers import TripSerializer, BookingSerializer, UserSerializer
from .utils import calculate_revenue

# Afficher pour créer un utilisateur
class RegisterUserView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.AllowAny]

# Afficher pour lister et créer des trajets.
class TripListCreateView(generics.ListCreateAPIView):
    queryset = Trip.objects.all()
    serializer_class = TripSerializer
    filter_fields = ['origin', 'destination', 'departure_datetime']
    # s'authentifiez avec un token
    authentication_classes = [authentication.TokenAuthentication]
    # appliquez la permission personnalisée permettant de créer un trajet en authentifiant 
    # ou soit de visualiser seulement la liste des trajets
    permission_classes = [IsAuthenticatedOrCreateOnly]
    
    # Surcharger la méthode pour retourner uniquement les trajets avec des places disponibles.
    def get_queryset(self):
        return Trip.objects.filter(available_seats__gt=0)


# Vue pour lister et créer des réservations.
class BookingListCreateView(generics.ListCreateAPIView):
    queryset = BooKing.objects.select_related('trip', 'author').all()
    serializer_class = BookingSerializer
    # Permettre à tout le monde de créer des réservations
    permission_classes = [permissions.AllowAny] 

    # Surcharger la méthode pour filtrer les réservations par trip_id 
    # si fourni dans les paramètres de requête.
    def get_queryset(self):
        trip_id = self.request.query_params.get('trip_id', None)
        if trip_id is not None:
            return BooKing.objects.filter(trip_id=trip_id)
        return super().get_queryset()
        

    # Créer une nouvelle réservation avec gestion de transaction pour assurer 
    # la cohérence et l'intégrité des données.
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        with transaction.atomic():
            trip = get_object_or_404(Trip, id=serializer.validated_data['trip'].id)
            num_seats = serializer.validated_data['num_seats']
            
            # Réduire le nombre de places disponibles dans le trajet
            trip.book_seats(num_seats)
            
            # Attribuer l'utilisateur à la réservation s'il est authentifié, sinon aucun
            user = request.user if request.user.is_authenticated else None
            serializer.save(author=user)

        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

# Vue pour récupérer le revenu pour un trajet spécifique.
class TripRevenueView(APIView):
    permission_classes = [permissions.IsAuthenticated] # Nécessite authentification

    # Récupérer et retourner le revenu pour le trajet spécifié.
    def get(self, request, trip_id):
        revenue = calculate_revenue(trip_id)
        return Response({'trip_id': trip_id, 'revenue': revenue})
