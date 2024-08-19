# Bus Ticket Booking System

Ce projet est un système de réservation de billets de bus développé avec Django et Django REST Framework. Il permet de gérer les trajets de bus et les réservations de sièges pour ces trajets.

## Introduction

L'objectif est de développer une application Django en mettant en œuvre les compétences suivantes :

- Utilisation de Django > 4 et Django Rest Framework (DRF)
- Programmation en Python 3 en respectant les conventions de style (Google/black/...)
- Respect des bonnes pratiques de Django et de DRF
- Utilisation des bibliothèques appropriées le cas échéant

## Consignes

L'objectif de ce projet est de développer une suite de services web destinés à une plateforme de réservation de tickets de bus. Il s'agit de mettre en place les modèles Django et les vues Django Rest Framework nécessaires pour implémenter l'API décrite ci-dessous.

### Contexte

L'entreprise exploite un service de réservation de tickets de bus en Afrique de l'Ouest. Ils souhaitent informatiser leur système de réservation et de suivi des trajets de bus.

### Modélisation

Concevoir des modèles Django pour représenter les entités du système de réservation de bus. 

### Les trajets

L'entreprise propose des trajets de bus avec des horaires fixes. L'endpoint `/api/trips/` permet de lister les différents trajets disponibles. Chaque trajet a une origine, une destination, une date et une heure de départ, ainsi qu'un nombre limité de places disponibles.

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

Il devrait être possible de filtrer les résultats par origine, destination et date de départ.

### API de réservation de tickets

L'endpoint `/api/bookings/` permettra aux utilisateurs de soumettre des réservations de tickets. Voici la structure attendue du payload pour effectuer une réservation :

### Payload de réservation

```json
{
    "trip": 1,
    "num_seats": 2
}
```

- `trip`: L'ID du trajet pour lequel le client souhaite réserver des places.
- `num_seats`: Le nombre de places que le client souhaite réserver.

## Exemple d'utilisation

### Exemple de réservation

Supposons que l'ID du premier trajet disponible est 1, et le client souhaite réserver 2 places.

**Requête :**

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

**Réponse (réussite) :**

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

#### Remarques

- Un utilisateur, même anonyme, peut effectuer une réservation.
- La réservation est créée avec un statut "pending" par défaut.
- La réservation est liée au trajet choisi.
- Si le nombre de places demandées dépasse le nombre de places disponibles dans le trajet, la réservation doit échouer avec un message d'erreur approprié.
- Une réservation ne peut pas être annulée ou modifiée via cette API. Une réservation peut être annulée ou modifiée en passant par une API distincte si cela est requis.

### Calcul de la rentabilité

Dans le cadre de l'application de réservation de tickets de bus, l'entreprise souhaite avoir un aperçu de la rentabilité de chaque trajet. Pour ça il faut calculer le revenu total généré par un trajet donné en fonction du nombre de réservations confirmées.

Implémentation d'une fonction Python qui prend en entrée l'ID d'un trajet et renvoie le revenu total généré par ce trajet. Supposons que la réservation d'un siège coûte un montant fixe, par exemple 1500 FCFA.

```python
def calculate_revenue(trip_id):
    """
    Calcule le revenu total généré par un trajet en fonction du nombre de réservations confirmées.

    :param trip_id: L'ID du trajet pour lequel calculer le revenu.
    :return: Le revenu total généré par le trajet.
    """
    # Reste du code
```

## Pour conclure

Pour que l'application soit fonctionnelle et fiable, des tests sont écrits pour vérifier son bon fonctionnement. L'utilisation de "factory-boy/Faker" ou de "fixtures" est recommandée pour charger des données en base de données lors de l'exécution des tests.

# Installation

Voici les étapes d'installation :

- Créez un environnement virtuel (`python3 -m venv .venv`)
- Activez l'environnement virtuel (`source .venv/bin/activate`)
- Installez les dépendances (`pip install -r requirements.txt`)
- Effectuez les migrations (`python busticket/manage.py migrate`)
- Lancez le serveur (`python busticket/manage.py runserver`)

## Travail accompli

## Fonctionnalités

- **Création et gestion des trajets de bus**
- **Réservation de sièges pour les trajets de bus**
- **Calcul des revenus pour chaque trajet**

## Installation

### Prérequis

- Python 3.10
- PostgreSQL (psycopg2-binary)
- Django 4.0.7
- Django REST Framework
- Django Extensions
- Django debug toolbar

### Outil tiers

Afin d'identifier et de résoudre rapidement les problèmes dans l'API, utilisez django debug toolbar pour le débogage qui fournissent des informations détaillées sur la requête et la réponse en cours, ainsi que sur l'état interne de l'API. 
Pour ça vous pouvez suivre les étapes mentionnés dans le documentation officiel `https://django-debug-toolbar.readthedocs.io/en/latest/`

### Étapes d'installation

1. Clonez le dépôt:

   ```bash
   git clone <URL-du-dépôt>
   cd bus-ticket-booking
   
2. Installez les dépendances:
   
   pip install -r requirements.txt
   
### 
   
3. Ajoutez les Applications au Projet
	Dans `busticket/settings.py`, ajouter `rest_framework` et `rides.apps.CoursesConfig` dans `INSTALLED_APPS`:
	
	```
		INSTALLED_APPS = [
	    		...
			    'rest_framework',
			    'rides.apps.CoursesConfig',
			...
	        ]
	```
	
4. Créez les Modèles Django
	Dans `rides/models.py`, définissez les modèles pour les trajets et les réservations:
	
	**Modèle Trip**:
	
	Le modèle `Trip` représente un trajet avec les champs suivants :
		`origin`: la ville de départ, `destination`: la ville d'arrivée, `departure_datetime`: la date et l'heure du départ,
		`available_seats`:le nombre de sièges disponibles pour le trajet
		
		La méthode `book_seats` permet de réserver des sièges pour un trajet s'il y en a suffisamment disponibles, en utilisant 
		`F()` pour gérer les problèmes de concurrence. 
		
		`unique_together`: permet de définir une contrainte d'unicité sur la combinaison des champs origin, destination et
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
	
	***Modèle Booking***:
	
	Le modèle `Booking` représente une réservation de sièges pour un trajet avec les champs suivants:
	`trip`: une référence au modèle `Trip`, `author`: une référence à l'utilisateur qui a fait la réservation, `num_seats`:le nombre de 
	sièges réservés, `status`: le statut de la réservation (`confirmed` ou `pending`)
	
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

	
7. Configurer de PostgreSQL
	Pour ce type de projet, il est généralement recommandé d'utiliser PostgreSQL
	
	
	- Installez PostgreSQL sur votre machine locale
	- Configurer votre base de données PostgreSQL dans `bus/settings.py`:

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

   

4. Faire les migrations
	python manage.py makemigrations
	python manage.py migrate
	
5. Créer un dossier package `api` à l'interieur du dossier package `rides` comme ci `rides/api` 
	**Configurer les URLs**
		Dans `rides/api/urls.py`, configurez les routes pour les API:
			Dans le module `urls.py` vous avez les endpoints suivantes:
			
			`trips/`: Route pour lister et créer des trajets
			`bookings/`: Route pour lister et créer des réservations
			`trip/revenue/<int:trip_id>/`:  Route pour récupérer le revenu d'un trajet spécifique
			`api_token_auth/` : Route pour créer un token après avoir été authentifier
			`register/`: Route pour créer des utilisateurs pouvant ainsi créer un trajet en utilisant POSTMAN ou INSOMNIA
			
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
	
		Ensuite, ajoutez l'url de l'API au projet principal dans `busticket/urls.py`:
		
		``` 	
			from django.contrib import admin
			from django.urls import path, include

			urlpatterns = [
			    path('admin/', admin.site.urls),
			    path('api/bus/', include('rides.api.urls')),
			]
		```
		
	**Créer les Sérializers**
		Dans `rides/api/serializers.py`, définissez les sérializers pour les trajets, les réservations et les utilisateurs:
			Le module `serializers.py` contient les serializers pour les modèles `Trip`, `Booking`, `User`. Les serializers 
			transforment les instances de modèles en formats de données tels que JSON pour les rendre utilisables
			par les API, et vice versa.
			
			**UserSerializer**
			Le `UserSerializer` sérialise le modèle `User` et inclut seulement les champs: `username` et `password`
			
			La méthode `create` permet créer un nouvel objet utilisateur et extrait le nom d'utilisateur et le mot de passe des
			données validées
			
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
			Le `TripSerializer` sérialise le modèle `Trip` et inclut les champs suivants : id, origin, destination, 	
			departure_datetime, et available_seats.
			
			- La méthode validate empêche la création de trajets en double avec la même origine, destination et horaire de 
			  départ.
			  
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
			  
			**BookingSerializer**
			Le `BookingSerializer` sérialise le modèle `Booking` et inclut les champs suivants : `id`, `trip`, `trip_id`, 
			`num_seats`, `status`, et `author`.  
			
			- `trip_id` utilise `PrimaryKeyRelatedField` pour permettre de référencer un `Trip` par son `ID`.
			- La méthode `validate_num_seats` vérifie que le nombre de sièges réservés est supérieur à zéro.
			- La méthode `validate` vérifie qu'il y a suffisamment de sièges disponibles dans le trajet choisi.
			- La méthode `create` ajoute l'auteur de la réservation à partir du contexte de la requête.
			
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
			
			`BookingSerializer` gère l'utilisateur anonyme dans la création de réservations:
			
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
			
	**Créer les Vues API**
		Dans `rides/api/views.py`, définissez les vues pour lister et créer les trajets et les réservations:
			Le module `views.py` contient les vues pour les modèles `User`, `Trip`, `Booking`, ainsi qu'une vue pour calculer 
			le revenu des trajets.
			
			**RegisterUserView**
			`RegisterUserView` est une vue basée sur les classes génériques de Django REST Framework pour créer des 
			 utilisateurs 
			
			```
				...
					class RegisterUserView(generics.CreateAPIView):
					    queryset = User.objects.all()
					    serializer_class = UserSerializer
					    permission_classes = [permissions.AllowAny]
				...
			```
			
			**TripListCreateView**
			`TripListCreateView` est une vue basée sur les classes génériques de Django REST Framework pour lister et créer des 
			trajets.Vous pouvez accéder à cette vue sans vous authentifié mais pour créer un trajet vous devez vous     		
			authentifiez afin d'obtenir un token qui sera utiliser pour créer un trajet d'ou utilisation de 
			`authentication.TokenAuthentication`
			
			- La méthode `get_queryset` est surchargée pour retourner uniquement les trajets avec des places disponibles.
			
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
			`BookingListCreateView` est une vue basée sur les classes génériques de Django REST Framework pour lister et créer 
			des réservations. Elle utilise l'attribut `permission_classes` pour définir les permissions d'accès à cette vue.
			
			- `permission_classes = [AllowAny]` signifie que tout le monde peut accéder à cette vue, qu'ils soient authentifiés 
			   ou non.
			- La méthode `get_queryset` est surchargée pour filtrer les réservations par `trip_id` si fourni dans les  	
			paramètres de requête.
			- La méthode `create` est surchargée pour gérer les transactions lors de la création de nouvelles réservations, 
			assurant la cohérence et l'intégrité des données.
			
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
			
6. Implémenter la Fonction de Calcul de la Rentabilité
	Dans rides/api/utils.py, créer la fonction calculer le revenu:
	
		```	from django.db.models import Sum
			from rides.models import BooKing

			def calculate_revenue(trip_id):
			    confirmed_bookings = BooKing.objects.filter(trip_id=trip_id, status='confirmed')
			    total_seats = confirmed_bookings.aggregate(Sum('num_seats'))['num_seats__sum']
			    if total_seats is None:
				return 0
			    return total_seats * 1500 
		    
		 ```
	Ensuite pour devez importer cette fonction dans `rides/api/views.py` afin de l'utiliser pour la fonction vue:
	`TripRevenueView` permet de récupérer le revenu pour un trajet spécifique en s'authentifiant d'ou utilisation
	`permission_classes = [permissions.IsAuthenticated]`.
			
	- la méthode `get` permet de récupérer et retourner le revenu pour le trajet spécifié en utilisant son id
	
	```
		class TripRevenueView(APIView):
		    permission_classes = [permissions.IsAuthenticated] 
		    
		    def get(self, request, trip_id):
			revenue = calculate_revenue(trip_id)
			return Response({'trip_id': trip_id, 'revenue': revenue})
	``` 
	
### Les Permissions

Concernant les permissions, il a été crée un fichier `permissions.py` contenant une fonction personnalisée permettant de restreindre l'accès à la vue `TripListCreateView` permettant d'afficher pour lister et créer des trajets:

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
cette fonction permet uniquement aux utilisateurs authentifiés de créer des objets. Tout le monde (authentifié ou non) peut lire les objets.Les modifications et suppressions sont interdites pour tout le monde.

Ensuite il est importé dans le module views.py pour être appliqué à la vue `TripListCreateView`:

```
	class TripListCreateView(generics.ListCreateAPIView):
		...
		
		    permission_classes = [IsAuthenticatedOrCreateOnly]
		...

```
    


Pour des raisons de sécurité de l'API il est plus adapté d'utiliser le Token Authentification ou JWT qui permet d'attribuer un token(en lui définissant une durée de vie) à l'utilsateur connecté afin de bénéficier d'une gestion centralisée des sessions et d'une expiration contrôlée des tokens, le Token Authentication pourrait être plus approprié. Cela permettra de gérer facilement les sessions utilisateur, d'implémenter des fonctionnalités comme la révocation de tokens si nécessaire, et de garantir une meilleure sécurité globale de l'application.

**Ajouter une application token**
Dans `busticket/settings.py`, ajouter `rest_framework.authtoken` dans `INSTALLED_APPS`:
	
	```
		INSTALLED_APPS = [
	    		...
			    'rest_framework.authtoken',
			...
	        ]
	```
Ensuite appliquer les migrations en utilisant la commande `python3 manage.py migrate`, une fois les migrations faites il faut se rendre dans `api/urls.py` pour définir la route de notre token:

```
	urlpatterns = [
	   ...
	    	path('api_token_auth/', obtain_auth_token, name='api-token-auth'),
	   ...
	]
```

Vous pouvez utiliser maintenant le token sur la vue approprié (`TripListCreateView`) : 
```
	class TripListCreateView(generics.ListCreateAPIView):
		...
		
		    authentication_classes = [authentication.TokenAuthentication]
		...

```
### Tester l'API
**Les Endpoints**

**/api/bus/trips/ : créer et lister les trajets**
**/api/bus/bookings/ : créer et lister les réservations**
**/api/bus/trip/revenue/<int:trip_id>/: lister le revenu pour un trajet spécifique**
**/api/bus/register/: créer des utilisateurs**
**/api/bus/api_token_auth/ : obtenir le token après authentification de l'utilisateur**

   
**Utilisation de Postman**
Pour tester l'API de manière efficace, Vous devez utiliser un outil tiers comme Postman, Insomnia,ou tout autre client HTTP pour tester l'API avec des en-têtes d'authentification:

**Création d'un endpoint pour utilisateur**

**endpoint: api/bus/register/**
Pour rendre le processus plus fluide pour les tests, nous allons gérer la création d'utilisateurs directement via votre API, pour ça il faut ajouter dans le module `serializers.py` la classe `UserSerializer` pour serializer nos données:
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
Ensuite rendez-vous dans le module `views.py` pour créer une vue `RegisterUserView` pour créer un utilisateur :

```
	class RegisterUserView(generics.CreateAPIView):
	    queryset = User.objects.all()
	    serializer_class = UserSerializer
	    permission_classes = [permissions.AllowAny]
```
**Configurer Postman pour créer un utilisateur**
- ouvrez Postman et cliquez sur New -> Request.
- donnez un nom à votre requête et sélectionnez ou créez une collection pour la sauvegarder
- dans l'onglet Enter request URL, entrez `http://<your_domain>/api/bus/register/`
- sélectionnez POST comme méthode HTTP
- cliquez sur l'onglet Body. Sélectionnez raw et choisissez JSON dans le menu déroulant
- collez le JSON suivant dans le corps de la requête :

```
	{
	  "username": "newuser",
	  "password": "newpassword"
	}

```
-cliquez sur Send.

**Création du token**
**endpoint: api/bus/api-token-auth/**
Pour utiliser Postman pour obtenir un token en envoyant les informations d'identification (nom d'utilisateur et mot de passe) à l'endpoint `/api-token-auth/`, suivez ces étapes :
	- Ouvrir Postman: Cliquez sur le bouton "New" ou "Create a request" pour créer une nouvelle requête
	-  Sélectionnez `POST`, Entrez l'URL de votre endpoint d'authentification, par exemple `http://<your_domain>/api_token_auth/`
	- Cliquez sur l'onglet `Body`, Sélectionnez `x-www-form-urlencoded`, Ajoutez deux clés : `username` et `password`, avec leurs  
	  correspondantes, Cliquez sur le bouton `Send`.
	- Si les informations d'identification sont correctes, vous recevrez une réponse contenant le token. La réponse ressemblera à 
	ceci :
	
	```
		{
		    "token": "your_generated_token"
		}
	```
	- 
**Utilisation du token pour créer les requêtes**
-Créez une nouvelle requête :
	* Ouvrez Postman.
	* Cliquez sur `New` -> `Request`
-Configurez la requête :
	* Sélectionnez POST comme méthode HTTP
	* Entrez l'URL de votre endpoint, par exemple http://your_domain/api/bus/trips/
-Ajoutez l'en-tête d'authentification :
	* Allez dans l'onglet `Headers`
	* Ajoutez un nouvel en-tête avec le Key `Authorization` et la `Value` `Token your_token`
5- Entrez les données de votre requête :
	* Allez dans l'onglet `Body`
	* Sélectionnez `raw`
	* Assurez-vous que le type est `JSON`
	* Entrez les données de votre requête en format JSON:
	```
		{
		    "origin": "Accra",
		    "destination": "Lomé",
		    "departure_datetime": "2024-07-06T12:00:00Z",
		    "available_seats": 30
		}

	```

### Tests Unitaires et Fonctionnels
Pour les tests un dossier package `tests` a été créé contenant les modules `test_models.py` et `test_views.py` contenant des tests unitaires et fonctionnels pour vérifier la bonne fonctionnalité des modèles et des vues de l'application.

**test_models.py**
Le module `test_models.py` contient des tests unitaires pour les modèles `Trip` et `Booking`. 
Voici un aperçu des tests réalisés :

## TripModelTests
	- `test_create_trip`: Vérifie la création d'un trajet
	- `test_trip_str`: Vérifie la représentation en chaîne de caractères d'un trajet
	- `test_booking_str`: Vérifie la représentation en chaîne de caractères d'une réservation
	- `test_create_booking`: Vérifie la création d'une réservation
	- `test_book_seats_success`: Vérifie la réservation de sièges avec succès
	- `test_book_seats_failure`: Vérifie l'échec de la réservation de sièges lorsque le nombre de sièges disponibles est insuffisant
	- `test_unique_together_constraint`: Vérifie la contrainte d'unicité pour la création de trajets avec la même origine, destination 
	   et horaire de départ
	   
**test_views.py**
Le module `test_views.py` contient des tests fonctionnels pour les vues `TripListCreateView`, `BookingListCreateView` et `TripRevenueView`. 
Voici un aperçu des tests réalisés :
	Liste des trajets disponibles
	Vérification de la réponse HTTP attendue (200 OK).
	Vérification du nombre de trajets retournés.
	Création d'un trajet (nécessite une authentification)
	Vérification de la réponse HTTP attendue pour la création (201 CREATED).
	Vérification de l'augmentation du nombre de trajets en base de données.
	Liste des réservations
	Vérification de la réponse HTTP attendue (200 OK).
	Vérification du nombre de réservations retournées (selon les données initiales).
	Filtrage des réservations par trajet
	Vérification de la réponse HTTP attendue (200 OK).
	Vérification du nombre de réservations retournées pour un trajet spécifique.
	Création d'une réservation
	Test avec un utilisateur authentifié
	Vérification de la réponse HTTP attendue pour la création (201 CREATED).
	Vérification des informations de la réservation créée.
	Vérification de la diminution des places disponibles du trajet concerné.
	Test avec un utilisateur anonyme
	Vérification de la réponse HTTP attendue pour la création (201 CREATED).
	Vérification des informations de la réservation créée (statut "pending").
	Vérification de la diminution des places disponibles du trajet concerné.
	Test avec un nombre de places insuffisant
	Vérification de la réponse HTTP d'erreur (400 Bad Request).
	Test avec un nombre de places négatif
	Vérification de la réponse HTTP d'erreur (400 Bad Request).
	Test avec un nombre de places nul
	Vérification de la réponse HTTP d'erreur (400 Bad Request).
	Calcul du revenu d'un trajet (nécessite une authentification)
	Vérification de la réponse HTTP attendue (200 OK).
	Vérification de la présence d'un champ "revenue" dans la réponse.

## Utilisation de fixtures pour des données spécifiques
Si vous avez besoin de données spécifiques pour vos tests, vous pouvez utiliser des fixtures Django. Les fixtures sont des fichiers JSON ou XML contenant des données de modèle prédéfinies.
	**Créez un fichier `tests/fixtures/initial_data.json`**
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
	Ensuite ces données sont chargés dans les tests `test_views.py` et `test_models.py`:
	
	**Exemple d'utilisation dans le fichier test_views.py**
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
	- `test_list_trips_with_available_seats`: Vérifie la liste des trajets avec des sièges disponibles.
	- `test_create_trip`: Vérifie la création d'un trajet.
	
## BookingListCreateViewTests
	- `test_list_bookings`: Vérifie la liste des réservations
	- `test_list_bookings_filtered_by_trip_id`: Vérifie la liste des réservations filtrées par `trip_id`
	- `test_create_booking_authenticated_user`: Vérifie la création d'une réservation par un utilisateur authentifié
	- `test_create_booking_anonymous_user`: Vérifie la création d'une réservation par un utilisateur anonyme
	- `test_create_booking_insufficient_seats`: Vérifie l'échec de la création d'une réservation lorsque le nombre de sièges 
	   disponibles est insuffisant
	- `test_create_booking_negative_seats`: Vérifie l'échec de la création d'une réservation avec un nombre de sièges négatif
	- `test_create_booking_zero_seats`: Vérifie l'échec de la création d'une réservation avec zéro siège

	
## TripRevenueViewTests
	- `test_get_trip_revenue`: Vérifie la récupération du revenu d'un trajet spécifique.
	


7. Tests des Modèles
	**Création de trajets et de réservations :**
		- Tester la création de trajets avec des attributs valides.
		- Tester la création de réservations avec des attributs valides.
		- Vérifier les relations entre les trajets et les réservations.
		


