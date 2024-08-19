# Bus Ticket Booking System

This project is a bus ticket reservation system developed using Django and the Django REST Framework. It manages bus journeys and seat reservations for these journeys.

## Introduction

The aim is to develop a Django application using the following skills:

- Use of Django > 4 and Django Rest Framework (DRF)
- Programming in Python 3, respecting style conventions (Google/black/...)
- Compliance with Django and DRF best practices
- Use of appropriate libraries where applicable

## Instructions

The aim of this project is to develop a suite of web services for a bus ticket reservation platform. It involves setting up the Django models and Django Rest Framework views needed to implement the API described below.

### Background

The company operates a bus ticket reservation service in West Africa. They wanted to computerise their system for booking and tracking bus journeys.

### Modelling

Design Django models to represent the entities of the bus reservation system. 

### The routes

The company offers bus routes with fixed timetables. The `/api/trips/` endpoint lists the different routes available. Each route has an origin, a destination, a departure date and time, and a limited number of available seats.

```json
[
    {
        "origin": "Abidjan",
        "destination": "Yamoussoukro",
        "departure_datetime": "2023-09-01T08:00:00",
        "available_seats": 15
    },
    {
        "origin": "Dakar",
        "destination": "Thiès",
        "departure_datetime": "2023-09-02T10:30:00",
        "available_seats": 10
    },
    ...
]
```

It should be possible to filter results by origin, destination and departure date.

### Ticket reservation API

The `/api/bookings/` endpoint will allow users to submit ticket reservations. Here is the expected structure of the payload for making a booking:

### Booking payload

```json
{
    "trip": 1,
    "num_seats": 2
}
```

- `trip`: The ID of the journey for which the customer wishes to reserve seats.
- `num_seats`: The number of seats the customer wishes to reserve.

## Example of use

### Reservation example

Suppose the ID of the first available journey is 1, and the customer wants to reserve 2 seats.

**Enquiry:**

```
POST /api/bookings/
```

**Payload :**

```json
{
    "trip": 1,
    "num_seats": 2
}
```

**Answer (pass):**

```json
{
    "id": 1,
    "trip": {
        "origin": "Abidjan",
        "destination": "Yamoussoukro",
        "departure_datetime": "2023-09-01T08:00:00",
        "available_seats": 15
    },
    "num_seats": 2,
    "status": "pending"
}
```

#### Notes

- A user, even an anonymous one, can make a reservation.
- The reservation is created with a default status of ‘pending’.
- The reservation is linked to the chosen route.
- If the number of seats requested exceeds the number of seats available on the route, the reservation must fail with an appropriate error message.
- A booking cannot be cancelled or modified via this API. A booking can be cancelled or modified via a separate API if required.

### Calculating profitability

As part of the bus ticket reservation application, the company wants to have an overview of the profitability of each journey. This involves calculating the total revenue generated by a given journey as a function of the number of confirmed bookings.

Implementation of a Python function which takes as input the ID of a journey and returns the total revenue generated by that journey. Let's assume that reserving a seat costs a fixed amount, for example 1500 FCFA.

```python
def calculate_revenue(trip_id):
    """
    Calculates the total revenue generated by a trip based on the number of confirmed bookings.

    :param trip_id: The ID of the trip for which to calculate revenue.
    :return: The total revenue generated by the trip.
    """
    # Reste du code
```

## To conclude

To ensure that the application is functional and reliable, tests are written to check that it is working properly. The use of ‘factory-boy/Faker’ or ‘fixtures’ is recommended for loading data into the database when running tests.

# Installation

Here are the installation steps:

- Create a virtual environment (`python3 -m venv .venv`)
- Activate the virtual environment (`source .venv/bin/activate`)
- Install the dependencies (`pip install -r requirements.txt`)
- Perform migrations (`python busticket/manage.py migrate`)
- Run the server (`python busticket/manage.py runserver`)

## Work done

## Features

- Creation and management of bus journeys** **Reservation of seats for bus journeys
- Reserving seats for bus journeys** **Calculating revenue for each journey
- Calculation of revenue for each journey** **Creation and management of bus journeys

## Installation

### Prerequisites

- Python 3.10
- PostgreSQL (psycopg2-binary)
- Django 4.0.7
- Django REST Framework
- Django Extensions
- Django debug toolbar

### Third-party tool

To quickly identify and resolve problems in the API, use the django debug toolbar for debugging, which provides detailed information about the current request and response, as well as the internal state of the API. 
To do this you can follow the steps mentioned in the official documentation `https://django-debug-toolbar.readthedocs.io/en/latest/`.

### Installation steps

1. Clone the repository:

   ```bash
   git clone https://github.com/Lyrecoph/busticket.git
   ```
2. Access the file

   cd bus-ticket-booking
   
3. Install the dependencies:
   
   pip install -r requirements.txt
   
### 
   
4. Add the Applications to the Project
	In `busticket/settings.py`, add `rest_framework` and `rides.apps.CoursesConfig` to `INSTALLED_APPS`:
	
	```
		INSTALLED_APPS = [
	    		...
			    'rest_framework',
			    'rides.apps.CoursesConfig',
			...
	        ]
	```
	
5. Create Django Templates
	In `rides/models.py`, define the templates for journeys and bookings:
	
	**Model Trip**:
	
	The `Trip` model represents a journey with the following fields:
		`origin`: the departure city, `destination`: the arrival city, `departure_datetime`: the departure date and time,
		available_seats`: the number of seats available for the journey.
		
		The `book_seats` method is used to reserve seats for a journey if enough are available, using 
		F()` to handle concurrency issues. 
		
		unique_together`: is used to define a uniqueness constraint on the combination of origin, destination and
		departure_datetime.
		
		```
			class Trip(models.Model):
			    origin = models.CharField(max_length=150)
			    destination = models.CharField(max_length=150)
			    departure_datetime = models.DateTimeField()
			    available_seats = models.IntegerField()

			    def __str__(self):
				return f'{self.origin} to {self.destination} on {self.departure_datetime}'

			    class Meta:
				verbose_name = 'Trajet'
				verbose_name_plural = 'Trajets'
				unique_together = ('origin', 'destination', 'departure_datetime')

			    def book_seats(self, num_seats):
				if self.available_seats >= num_seats:
				    self.available_seats = F('available_seats') - num_seats
				    self.save()
				    return True
				return False
		```
	
	***Model Booking***:
	
	The `Booking` model represents a seat reservation for a journey with the following fields:

	`trip`: a reference to the `Trip` model, 

	`author`: a reference to the user who made the reservation, 
	
	`num_seats`: the number of seats reserved, 

	`status`: the status of the reservation (`confirmed` or `pending`)
	
	```
		class Booking(models.Model):
		    STATUS_CHOICES = (
			('confirmed', 'Confirmed'),
			('pending', 'Pending')
		    )
		    trip = models.ForeignKey(Trip, on_delete=models.CASCADE, related_name='bookings')
		    author = models.ForeignKey(User, null=True, blank=True, on_delete=models.SET_NULL)
		    num_seats = models.IntegerField(null=True)
		    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending')

		    def __str__(self):
			return f'Booking for {self.num_seats} seats on {self.trip}'

		    class Meta:
			verbose_name = 'Reservation'
			verbose_name_plural = 'Reservations'
	```

	
6. Configuring PostgreSQL
	For this type of project, we generally recommend using PostgreSQL
	
	- Install PostgreSQL on your local machine
	- Configure your PostgreSQL database in `bus/settings.py`:

		```
			...
				DATABASES = {
				    	"default": {
						"ENGINE": "django.db.backends.postgresql",
						"NAME": "busticket",
						"USER": "youruser",
						"PASSWORD": "yourpassword",
						"HOST": "localhost",
						"PORT": 5432,
				    	}
			 	}
			...
	        ```

   

7. Migration
	python manage.py makemigrations
	python manage.py migrate
	
8. Create an `api` package folder inside the `rides` package folder as `rides/api`. 

	**Configure URLs**
		In `rides/api/urls.py`, configure the routes for the APIs:
			In the `urls.py` module you have the following endpoints:
			
			`trips/`: Route to list and create trips
			`bookings/`: Route to list and create bookings
			`trip/revenue/<int:trip_id>/`: Route to retrieve revenue for a specific trip
			`api_token_auth/`: Route to create a token after authentication
			`register/`: Route to create users who can then create a trip using POSTMAN or INSOMNIA
			
			```
				...
					urlpatterns = [
					    path('trips/', TripListCreateView.as_view(), name='trip-list-create'),
					    path('trip/revenue/<int:trip_id>/', TripRevenueView.as_view(), name='trip-revenue'),
					    path('api_token_auth/', obtain_auth_token, name='api-token-auth'),
					    path('register/', RegisterUserView.as_view(), name='register-user'),    
					]
				...
			```
	
		Next, add the API url to the main project in `busticket/urls.py`:
		
		``` 	
			from django.contrib import admin
			from django.urls import path, include

			urlpatterns = [
			    path('admin/', admin.site.urls),
			    path('api/bus/', include('rides.api.urls')),
			]
		```
		
	**Create Serializers** 

		In `rides/api/serializers.py`, define serializers for trips, bookings and users:
			The `serializers.py` module contains serializers for the `Trip`, `Booking`, `User` models. Serializers 
			transform model instances into data formats such as JSON to make them usable by the
			APIs, and vice versa.
			
			**UserSerializer**
			The `UserSerializer` serializes the `User` model and includes only the fields: `username` and `password`.
			
			The `create` method creates a new user object and extracts the username and password from the validated data
			
			```
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
			```
			
			**TripSerializer** 
			The TripSerializer serializes the Trip model and includes the following fields: id, origin, destination, departure_datetime, and available_seats.
			
			- The validate method prevents the creation of duplicate journeys with the same origin, destination and departure time.
			  
			```
				class TripSerializer(serializers.ModelSerializer):
				    class Meta:
					model = Trip
					fields = ['id', 'origin', 'destination', 'departure_datetime', 'available_seats']

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
			```
			  
			**LookingSerializer**
			The `BookingSerializer` serializes the `Booking` template and includes the following fields: `id`, `trip`, `trip_id`, `num_seats`, `status`, and `author`.  
			
			- `trip_id` uses `PrimaryKeyRelatedField` to allow a `Trip` to be referenced by its `ID`.
			- The `validate_num_seats` method checks that the number of seats reserved is greater than zero.
			- The `validate` method checks that there are enough seats available on the chosen route.
			- The `create` method adds the author of the reservation from the request context.
			
			```
				
				class BookingSerializer(serializers.ModelSerializer):
				    trip = TripSerializer(read_only=True)
				    trip_id = serializers.PrimaryKeyRelatedField(
					queryset=Trip.objects.all(), write_only=True, source='trip'
				    )

				    class Meta:
					model = BooKing
					fields = ['id', 'trip', 'trip_id', 'num_seats', 'status', 'author']
					read_only_fields = ['status', 'author']

				    def validate_num_seats(self, value):
					if value <= 0:
					    raise serializers.ValidationError(
						'Number of seats must be greater than zero.'
					    )
					return value

				    def validate(self, data):
					trip = data['trip']
					num_seats = data['num_seats']
					if trip.available_seats < num_seats:
					    raise serializers.ValidationError(
						'Not enough available seats for this trip.'
					    )
					return data
			```
			
			The `BookingSerializer` manages the anonymous user in the creation of bookings:
			
			```
				class BookingSerializer(serializers.ModelSerializer):
					...
						def create(self, validated_data):
							user = self.context['request'].user if 
							self.context['request'].user.is_authenticated else None
							validated_data['author'] = user
							return super().create(validated_data)
					...
			```
			
	**Creating API Views**

		In `rides/api/views.py`, define the views for listing and creating journeys and bookings:
			The `views.py` module contains views for the `User`, `Trip`, `Booking` models, as well as a view for calculating income from trips.
			
			**RegisterUserView**
			RegisterUserView is a view based on the generic Django REST Framework classes for creating users. 
			
			```
				...
					class RegisterUserView(generics.CreateAPIView):
					    queryset = User.objects.all()
					    serializer_class = UserSerializer
					    permission_classes = [permissions.AllowAny]
				...
			```
			
			**TripListCreateView**
				TripListCreateView is a view based on the generic Django REST Framework classes for listing and creating trips. 
				You can access this view without authenticating, but to create a trip you need to authenticate to get a token.     		
				You can access this view without authenticating but to create a path you need to authenticate in order to obtain a token which will be used to create a path. 
				`authentication.TokenAuthentication`
			
			- The `get_queryset` method is overloaded to return only journeys with available seats.
			
			```
				class TripListCreateView(generics.ListCreateAPIView):
				    queryset = Trip.objects.all()
				    serializer_class = TripSerializer
				    filter_fields = ['origin', 'destination', 'departure_datetime']
				    authentication_classes = [authentication.TokenAuthentication]
				    permission_classes = [IsAuthenticatedOrCreateOnly]
				    
				    def get_queryset(self):
        				return Trip.objects.filter(available_seats__gt=0)
			```
			
			**BookingListCreateView**
			The `BookingListCreateView` is a view based on the generic Django REST Framework classes for listing and creating 
			reservations. It uses the `permission_classes` attribute to define access permissions to this view.
			
			- `permission_classes = [AllowAny]` means that anyone can access this view, whether they are authenticated authenticated or not.
			- The `get_queryset` method is overloaded to filter reservations by `trip_id` if supplied in the query parameters.
			- The `create` method is overloaded to manage transactions when new reservations are created, ensuring data consistency and integrity.
			
			```
				class BookingListCreateView(generics.ListCreateAPIView):
				    queryset = BooKing.objects.select_related('trip', 'author').all()
				    serializer_class = BookingSerializer
				    permission_classes = [permissions.AllowAny]

				    def get_queryset(self):
					trip_id = self.request.query_params.get('trip_id', None)
					if trip_id is not None:
					    return BooKing.objects.filter(trip_id=trip_id)
					return super().get_queryset()

				    def create(self, request, *args, **kwargs):
					serializer = self.get_serializer(data=request.data)
					serializer.is_valid(raise_exception=True)
					
					with transaction.atomic():
					    trip = get_object_or_404(Trip, id=serializer.validated_data['trip'].id)
					    num_seats = serializer.validated_data['num_seats']
					    trip.book_seats(num_seats)
					    
					    user = request.user if request.user.is_authenticated else None
            					   serializer.save(author=user)
					headers = self.get_success_headers(serializer.data)
					return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

			```
			
9. Implement the Profitability Calculation Function
	In rides/api/utils.py, create the calculate income function:
	
		```	from django.db.models import Sum
			from rides.models import BooKing

			def calculate_revenue(trip_id):
			    confirmed_bookings = BooKing.objects.filter(trip_id=trip_id, status='confirmed')
			    total_seats = confirmed_bookings.aggregate(Sum('num_seats'))['num_seats__sum']
			    if total_seats is None:
				return 0
			    return total_seats * 1500 
		    
		 ```
	Then you need to import this function into `rides/api/views.py` in order to use it for the view function:
	`TripRevenueView` allows you to retrieve revenue for a specific trip by authenticating or using
	`permission_classes = [permissions.IsAuthenticated]`.
			
	- the `get` method is used to retrieve and return the revenue for the specified route using its id
	
	```
		class TripRevenueView(APIView):
		    permission_classes = [permissions.IsAuthenticated] 
		    
		    def get(self, request, trip_id):
			revenue = calculate_revenue(trip_id)
			return Response({'trip_id': trip_id, 'revenue': revenue})
	``` 
	
### Permissions

With regard to permissions, a `permissions.py` file has been created, containing a custom function for restricting access to the `TripListCreateView` view, which is used to display, list and create routes:

```
	class IsAuthenticatedOrCreateOnly(BasePermission):
	    
	    def has_permission(self, request, view):
		if request.method in SAFE_METHODS:
		    return True
		elif request.method == 'POST':
		    return request.user and request.user.is_authenticated
		else:
		    return False
```
This function only allows authenticated users to create objects. Anyone (authenticated or not) can read the objects, and modifications and deletions are prohibited for everyone.

It is then imported into the views.py module and applied to the `TripListCreateView`:

```
	class TripListCreateView(generics.ListCreateAPIView):
		...
		
		    permission_classes = [IsAuthenticatedOrCreateOnly]
		...

```
    


For API security reasons, it would be more appropriate to use Token Authentication or JWT, which enables a token to be allocated (with a defined lifetime) to the connected user, in order to benefit from centralised session management and controlled token expiry. This will make it easier to manage user sessions, implement features such as token revocation if necessary, and guarantee better overall security for the application.

**Add a token application**
In `busticket/settings.py`, add `rest_framework.authtoken` to `INSTALLED_APPS`:
	
	```
		INSTALLED_APPS = [
	    		...
			    'rest_framework.authtoken',
			...
	        ]
	```
Then apply the migrations using the `python3 manage.py migrate` command. Once the migrations are done, we need to go to `api/urls.py` to define the route for our token:

```
	urlpatterns = [
	   ...
	    	path('api_token_auth/', obtain_auth_token, name='api-token-auth'),
	   ...
	]
```

You can now use the token on the appropriate view (`TripListCreateView`) : 

```
	class TripListCreateView(generics.ListCreateAPIView):
		...
		
		    authentication_classes = [authentication.TokenAuthentication]
		...

```
### Testing the API
**Endpoints**

**/api/bus/trips/ : create and list journeys** 
**/api/bus/bookings/ : create and list bookings**
**/api/bus/bookings/ : create and list bookings** 
**/api/bus/trip/revenue/<int:tripid> : create and list trips**
**/api/bus/trip/revenue/<int:trip_id>/: list revenue for a specific trip** 
**/api/bus/bookings/: create and list bookings**
**/api/bus/register/: create users**
**/api/bus/api_token_auth/: obtain token after user authentication**

   
**Using Postman**
To test the API effectively, you need to use a third-party tool such as Postman, Insomnia or any other HTTP client to test the API with authentication headers:

**Create an endpoint for a user**

**endpoint: api/bus/register/**
To make the process smoother for the tests, we're going to manage the creation of users directly via your API. To do this, we need to add the `UserSerializer` class to the `serializers.py` module to serialise our data:

```
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
``` 
Then go to the `views.py` module to create a `RegisterUserView` to create a user:

```
	class RegisterUserView(generics.CreateAPIView):
	    queryset = User.objects.all()
	    serializer_class = UserSerializer
	    permission_classes = [permissions.AllowAny]
```
**Configure Postman to create a user**.
- open Postman and click on New -> Request.
- give your request a name and select or create a collection to save it in
- in the Enter request URL tab, enter `http://<your_domain>/api/bus/register/`
- select POST as the HTTP method
- click on the Body tab. Select raw and choose JSON from the drop-down menu
- paste the following JSON into the request body:

```
	{
	  "username": "newuser",
	  "password": "newpassword"
	}

```
-click on Send.


**endpoint: api/bus/api-token-auth/**
To use Postman to obtain a token by sending credentials (username and password) to the `api-token-auth/` endpoint, follow these steps:
	- Open Postman: Click on the ‘New’ or ‘Create a request’ button to create a new request.
	- Select `POST`, Enter the URL of your authentication endpoint, for example `http://<your_domain>/api_token_auth/`
	- Click on the `Body` tab, Select `x-www-form-urlencoded`, Add two keys: `username` and `password`, with their  
	  Click on the `Send` button.
	- If the credentials are correct, you will receive a response containing the token. The response will look like 
	like this:
	
	```
		{
		    "token": "your_generated_token"
		}
	```
	- 
**Using the token to create queries**
-Create a new request:
	* Open Postman.
	* Click on `New` -> `Request`.
-Configure the request:
	* Select POST as the HTTP method
	* Enter the URL of your endpoint, for example http://your_domain/api/bus/trips/
-Add the authentication header:
	* Go to the `Headers` tab
	* Add a new header with the Key `Authorization` and the `Value` `Token your_token`.
5- Enter your request data:
	* Go to the `Body` tab
	* Select `raw
	* Make sure the type is `JSON`.
	* Enter your request data in JSON format:
	```
		{
		    "origin": "Accra",
		    "destination": "Lomé",
		    "departure_datetime": "2024-07-06T12:00:00Z",
		    "available_seats": 30
		}

	```

### Unit and Functional Tests
For the tests, a `tests` package folder has been created containing the `test_models.py` and `test_views.py` modules, which contain unit and functional tests to check the correct functionality of the application's models and views.

**test_models.py**
The `test_models.py` module contains unit tests for the `Trip` and `Booking` models. 
Here is an overview of the tests performed:

## TripModelTests
	- `test_create_trip`: Checks the creation of a trip
	- test_trip_str`: checks the string representation of a trip
	- test_booking_str`: Checks the string representation of a booking
	- test_create_booking`: checks the creation of a booking
	- test_book_seats_success`: Checks for successful seat booking
	- test_book_seats_failure: Checks for a failed seat reservation when there are not enough seats available.
	- test_unique_together_constraint`: Checks the uniqueness constraint for creating journeys with the same origin, destination and departure time
	   
**test_views.py**
The `test_views.py` module contains functional tests for the `TripListCreateView`, `BookingListCreateView` and `TripRevenueView` views. 
Here is an overview of the tests carried out:
	List of available routes
	Checking the expected HTTP response (200 OK).
	Checking the number of trips returned.
	Creating a route (requires authentication)
	Checking the expected HTTP response for creation (201 CREATED).
	Checking the increase in the number of trips in the database.
	List of reservations
	Checking the expected HTTP response (200 OK).
	Verification of the number of returned reservations (based on initial data).
	Filtering reservations by route
	Checking the expected HTTP response (200 OK).
	Checking the number of returned reservations for a specific trip.
	Creating a reservation
	Test with an authenticated user
	Checking the expected HTTP response for creation (201 CREATED).
	Checking the information of the created reservation.
	Verification of the reduction in available places on the route concerned.
	Test with an anonymous user
	Checking the expected HTTP response for creation (201 CREATED).
	Verification of the information of the reservation created (“pending” status).
	Verification of the reduction in available places on the route concerned.
	Test with insufficient number of places
	Checking the HTTP error response (400 Bad Request).
	Test with a negative number of places
	Checking the HTTP error response (400 Bad Request).
	Test with zero number of places
	Checking the HTTP error response (400 Bad Request).
	Calculating trip income (requires authentication)
	Checking the expected HTTP response (200 OK).
	Checking the presence of a "revenue" field in the response.

## Using fixtures for specific data
If you need specific data for your tests, you can use Django fixtures. Fixtures are JSON or XML files containing predefined model data.
**Create a `tests/fixtures/initial_data.json` file**
	```
		[
			....
				{
					"model": "rides.trip",
					"pk": 6,
					"fields": {
					    "origin": "Abidjan",
					    "destination": "Bouaké",
					    "departure_datetime": "2024-09-01T09:00:00",
					    "available_seats": 0
					}
				    },
				    {
					"model": "rides.booking",
					"pk": 1,
					"fields": {
					    "trip": 1,
					    "author": 1,
					    "num_seats": 2,
					    "status": "confirmed"
					}
				    },
				    {
					"model": "rides.booking",
					"pk": 2,
					"fields": {
					    "trip": 3,
					    "author": 1,
					    "num_seats": 3,
					    "status": "pending"
					}
				    },
				}
			...
		]
	```
	Then this data is loaded into the tests `test_views.py` and `test_models.py`:
	
	**Example of use in the test_views.py file**
	``` 
		...
			class TripListCreateViewTests(APITestCase):
			    fixtures = ['initial_data.json']

			    def test_list_trips_with_available_seats(self):
				url = reverse('trip-list-create')
				response = self.client.get(url, format='json')
				self.assertEqual(response.status_code, status.HTTP_200_OK)
				self.assertEqual(len(response.data), 5)
		... 
	```

## TripListCreateViewTests
	- `test_list_trips_with_available_seats`: Checks the list of trips with available seats.
	- `test_create_trip`: Checks the creation of a trip.
	
## BookingListCreateViewTests
	- `test_list_bookings`: Checks the list of reservations
	- `test_list_bookings_filtered_by_trip_id`: Checks the list of reservations filtered by `trip_id`
	- `test_create_booking_authenticated_user`: Checks the creation of a reservation by an authenticated user
	- `test_create_booking_anonymous_user`: Checks the creation of a reservation by an anonymous user
	- `test_create_booking_insufficient_seats`: Checks for failure to create a reservation when the number of seats 
	   available is insufficient
	- `test_create_booking_negative_seats`: Checks for failure to create a reservation with a negative number of seats
	- `test_create_booking_zero_seats`: Checks for failure to create a reservation with zero seats

	
## TripRevenueViewTests
	- `test_get_trip_revenue`: Checks the income recovery of a specific trip.
	


10. Model Testing
	**Creation of trips and reservations:**
		- Test the creation of routes with valid attributes.
		- Test the creation of reservations with valid attributes.
		- Check the relationships between trips and reservations.
		


