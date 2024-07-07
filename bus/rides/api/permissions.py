from rest_framework.permissions import BasePermission, SAFE_METHODS

class IsAuthenticatedOrCreateOnly(BasePermission):
    """
    Autorisation personnalisée pour permettre uniquement aux utilisateurs authentifiés 
    de créer des objets. Tout le monde (authentifié ou non) peut lire les objets.
    Les modifications et suppressions sont interdites pour tout le monde.
    """
    def has_permission(self, request, view):
        if request.method in SAFE_METHODS:
            # Lecture (GET, HEAD, OPTIONS) est permise pour tout le monde
            return True
        elif request.method == 'POST':
            # Création (POST) est permise seulement pour les utilisateurs authentifiés
            return request.user and request.user.is_authenticated
        else:
            # Modification et suppression (PUT, PATCH, DELETE) sont interdites pour tout le monde
            return False
