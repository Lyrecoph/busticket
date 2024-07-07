# factories.py

import factory
from django.utils import timezone
from .models import Trip, Booking

class TripFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Trip

    origin = factory.Faker('city')
    destination = factory.Faker('city')
    departure_datetime = factory.Faker('future_datetime', end_date='+30d', tzinfo=timezone.utc)
    available_seats = factory.Faker('random_int', min=1, max=50)

class BookingFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Booking

    trip = factory.SubFactory(TripFactory)
    num_seats = factory.Faker('random_int', min=1, max=5)
    status = 'pending'
