from django.urls import path

from rest_framework.authtoken.views import obtain_auth_token

from .views import TripListCreateView, BookingListCreateView, TripRevenueView, RegisterUserView

urlpatterns = [
    path('trips/', TripListCreateView.as_view(), name='trip-list-create'),
    path('bookings/', BookingListCreateView.as_view(), name='booking-list-create'),
    path('trip/revenue/<int:trip_id>/', TripRevenueView.as_view(), name='trip-revenue'),
    path('api_token_auth/', obtain_auth_token, name='api-token-auth'),
    path('register/', RegisterUserView.as_view(), name='register-user'),
]
