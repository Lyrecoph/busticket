from django.db.models import Sum

from rides.models import BooKing

def calculate_revenue(trip_id):
    confirmed_bookings = BooKing.objects.filter(trip_id=trip_id, status='confirmed')
    total_seats = confirmed_bookings.aggregate(Sum('num_seats'))['num_seats__sum']
    if total_seats is None:
        return 0
    return total_seats * 1500 