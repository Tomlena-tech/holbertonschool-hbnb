from app.persistence.repositories import UserRepository, PlaceRepository, ReviewRepository, AmenityRepository
from app.models.user import User
from app.models.amenity import Amenity
from app.models.place import Place
from app.models.review import Review


class HBnBFacade:

    """
    Classe de façade qui centralise l'accès aux dépôts mémoire
    pour les entités principales (User, Place, Review, Amenity).
    """

    def __init__(self):

        """
        Initialise les différents dépôts en mémoire.
        """

        self.user_repo = UserRepository()
        self.place_repo = PlaceRepository()
        self.review_repo = ReviewRepository()
        self.amenity_repo = AmenityRepository()

    def create_user(self, user_data):
        user = User(**user_data)
        self.user_repo.add(user)
        return user

    def get_user(self, user_id):
        return self.user_repo.get(user_id)

    def get_user_by_email(self, email):
        return self.user_repo.get_by_attribute('email', email)

    def get_all_users(self):
        return self.user_repo.get_all()

    def update_user(self, user_id, user_data):
        self.user_repo.update(user_id, user_data)
        return self.user_repo.get(user_id)

    def create_amenity(self, amenity_data):
        amenity = Amenity(**amenity_data)
        self.amenity_repo.add(amenity)
        return amenity

    def get_amenity(self, amenity_id):
        return self.amenity_repo.get(amenity_id)

    def get_all_amenities(self):
        return self.amenity_repo.get_all()

    def update_amenity(self, amenity_id, amenity_data):
        self.amenity_repo.update(amenity_id, amenity_data)
        return self.amenity_repo.get(amenity_id)

    def create_place(self, place_data):
        owner_id = place_data.get('owner_id')
        owner = self.user_repo.get(owner_id)
        if not owner:
            return None

        amenity_ids = place_data.get('amenities', [])

        place = Place(
            title=place_data['title'],
            description=place_data.get('description'),
            price=place_data['price'],
            latitude=place_data['latitude'],
            longitude=place_data['longitude'],
            owner_id=owner_id
        )

        for amenity_id in amenity_ids:
            amenity = self.amenity_repo.get(amenity_id)
            if amenity:
                place.add_amenity(amenity)

        self.place_repo.add(place)
        return place

    def get_place(self, place_id):
        return self.place_repo.get(place_id)

    def get_all_places(self):
        return self.place_repo.get_all()

    def update_place(self, place_id, place_data):
        self.place_repo.update(place_id, place_data)
        return self.place_repo.get(place_id)

    def create_review(self, review_data):
        user_id = review_data.get('user_id')
        place_id = review_data.get('place_id')

        user = self.user_repo.get(user_id)
        place = self.place_repo.get(place_id)

        if not user or not place:
            return None
        
        if user_id == place.owner_id:
            raise ValueError("Cannot review your own place")
        
        existing_reviews = self.review_repo.get_by_place(place_id)
        for review in existing_reviews:
           if review.user_id == user_id:
            raise ValueError("You have already reviewed this place")

        review = Review(
            text=review_data['text'],
            rating=review_data['rating'],
            place_id=place_id,
            user_id=user_id
        )

        self.review_repo.add(review)
        return review

    def get_review(self, review_id):
        return self.review_repo.get(review_id)

    def get_all_reviews(self):
        return self.review_repo.get_all()

    def get_reviews_by_place(self, place_id):
        return self.revierepo.gereviews_by_place(place_id)

    def update_review(self, review_id, review_data):
        self.review_repo.update(review_id, review_data)
        return self.review_repo.get(review_id)

    def delete_review(self, review_id):
        review = self.review_repo.get(review_id)
        if not review:
            return False
        self.review_repo.delete(review_id)
        return True
