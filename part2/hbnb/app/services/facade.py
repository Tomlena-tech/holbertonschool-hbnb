from app.persistence.repository import InMemoryRepository
from app.models.user import User
from app.models.place import Place
from app.models.review import Review
from app.models.amenity import Amenity

# ------------------------------------------------------------
# Classe de façade principale : interface entre API et logique
# ------------------------------------------------------------


class HBnBFacade:

    """
    Classe de façade qui centralise l'accès aux dépôts mémoire
    pour les entités principales (User, Place, Review, Amenity).
    """

    def __init__(self):

        """
        Initialise les différents dépôts en mémoire.
        """

        self.user_repo = InMemoryRepository()
        self.place_repo = InMemoryRepository()
        self.review_repo = InMemoryRepository()
        self.amenity_repo = InMemoryRepository()

# ----------------------------------------
# ---------- USER METHODS ----------------
# ----------------------------------------

    def create_user(self, user_data):

        """
        Crée un nouvel utilisateur et l'ajoute au dépôt.
        """

        user = User(**user_data)
        self.user_repo.add(user)
        return user

# ------------------------------------------------------------

    def get_user(self, user_id):

        """
        Récupère un utilisateur par son ID.
        """

        return self.user_repo.get(user_id)

# ------------------------------------------------------------

    def get_user_by_email(self, email):

        """
        Récupère un utilisateur à partir de son email.
        """

        return self.user_repo.get_by_attribute('email', email)

# ------------------------------------------------------------

    def get_all_users(self):

        """
        Retourne la liste de tous les utilisateurs.
        """

        return self.user_repo.get_all()

# ------------------------------------------------------------

    def update_user(self, user_id, user_data):

        """
        Met à jour les informations d'un utilisateur.
        """

        user = self.user_repo.get(user_id)
        if not user:
            return None

        for key, value in user_data.items():
            setattr(user, key, value)

        self.user_repo.update(user)
        return user

# -------------------------------------------
# ---------- AMENITY METHODS ----------------
# -------------------------------------------

    def create_amenity(self, amenity_data):

        """
        Crée une commodité et l'ajoute au dépôt.
        """

        amenity = Amenity(**amenity_data)
        self.amenity_repo.add(amenity)
        return amenity

# ------------------------------------------------------------

    def get_amenity(self, amenity_id):

        """
        Récupère une commodité à partir de son ID.
        """

        return self.amenity_repo.get(amenity_id)

# ------------------------------------------------------------

    def get_all_amenities(self):

        """
        Retourne la liste de toutes les commodités.
        """

        return self.amenity_repo.get_all()

# ------------------------------------------------------------

    def update_amenity(self, amenity_id, amenity_data):

        """
        Met à jour les informations d'une commodité.
        """

        amenity = self.amenity_repo.get(amenity_id)
        if not amenity:
            return None

        for key, value in amenity_data.items():
            setattr(amenity, key, value)

        self.amenity_repo.update(amenity)
        return amenity

# -----------------------------------------
# ---------- PLACE METHODS ----------------
# -----------------------------------------

    def create_place(self, place_data):

        """
        Crée un nouveau lieu avec ses attributs de base.
        """

        place = Place(**place_data)
        self.place_repo.add(place)
        return place

# ------------------------------------------------------------

    def get_place(self, place_id):

        """
        Récupère un lieu par son ID.
        """

        return self.place_repo.get(place_id)

# ------------------------------------------------------------

    def get_all_places(self):

        """
        Retourne la liste de tous les lieux.
        """

        return self.place_repo.get_all()

# ------------------------------------------------------------

    def update_place(self, place_id, place_data):

        """
        Met à jour les informations d'un lieu existant.
        """

        place = self.place_repo.get(place_id)
        if not place:
            return None

        for key, value in place_data.items():
            setattr(place, key, value)

        self.place_repo.update(place)
        return place

# ------------------------------------------
# ---------- REVIEW METHODS ----------------
# ------------------------------------------

    def create_review(self, review_data):

        """
        Crée un nouvel avis et l'ajoute au dépôt.
        """

        review = Review(**review_data)
        self.review_repo.add(review)
        return review

# ------------------------------------------------------------

    def get_review(self, review_id):

        """
        Récupère un avis à partir de son ID.
        """

        return self.review_repo.get(review_id)

# ------------------------------------------------------------

    def get_all_reviews(self):

        """
        Retourne la liste de tous les avis.
        """

        return self.review_repo.get_all()

# ------------------------------------------------------------

    def get_reviews_by_place(self, place_id):

        """
        Récupère tous les avis associés à un lieu donné.
        """

        all_reviews = self.review_repo.get_all()
        filtered_reviews = []
        for r in all_reviews:
            if r.place_id == place_id:
                filtered_reviews.append(r)

        return filtered_reviews

# ------------------------------------------------------------

    def update_review(self, review_id, review_data):

        """
        Met à jour un avis existant.
        """

        review = self.review_repo.get(review_id)
        if not review:
            return None
        for key, value in review_data.items():
            setattr(review, key, value)

        self.review_repo.update(review)
        return review

# ------------------------------------------------------------

    def delete_review(self, review_id):

        """
        Supprime un avis du dépôt.
        """

        review = self.review_repo.get(review_id)
        if not review:
            return None
        self.review_repo.delete(review_id)
        return review
# ------------------------------------------------------------
