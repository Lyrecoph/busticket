from django.contrib.auth.models import User

from rest_framework import serializers
from rides.models import Trip, BooKing

# Serializer pour le modèle User 
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'password']
    password = serializers.CharField(write_only=True)

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
            password=validated_data['password'],
        )
        return user

# Serializer pour le modèle Trip.
class TripSerializer(serializers.ModelSerializer):
    class Meta:
        model = Trip
        fields = ['id', 'origin', 'destination', 'departure_datetime', 'available_seats']


    # Valide les données pour éviter la création de trajets en double 
    # avec les mêmes origine, destination et horaire de départ.
    def validate(self, data):
        if Trip.objects.filter(
            origin=data['origin'],  
            destination=data['destination'],
            departure_datetime=data['departure_datetime']
        ).exists():
            raise serializers.ValidationError(
                'A trip with the same origin, destination, and departure time already exists.'
            )
        return data

# Serializer pour le modèle BooKing.
class BookingSerializer(serializers.ModelSerializer):
    trip = TripSerializer(read_only=True)
    trip_id = serializers.PrimaryKeyRelatedField(
        queryset=Trip.objects.all(), write_only=True, source='trip'
    )

    class Meta:
        model = BooKing
        fields = ['id', 'trip', 'trip_id', 'num_seats', 'status', 'author']
        read_only_fields = ['status', 'author']


    # Valide le nombre de sièges pour s'assurer qu'il est supérieur à zéro.
    def validate_num_seats(self, value):
        if value <= 0:
            raise serializers.ValidationError(
                'Number of seats must be greater than zero.'
            )
        return value

    # Valide les données de réservation pour s'assurer qu'il y a suffisamment de sièges 
    # disponibles dans le trajet choisi.
    def validate(self, data):
        trip = data['trip']
        num_seats = data['num_seats']
        if trip.available_seats < num_seats:
            raise serializers.ValidationError(
                'Not enough available seats for this trip.'
            )
        return data
    
    # Crée une nouvelle réservation en ajoutant l'auteur de la réservation 
    # à partir du contexte de la requête.
    def create(self, validated_data):
        user = self.context['request'].user if self.context['request'].user.is_authenticated else None
        validated_data['author'] = user
        return super().create(validated_data)
