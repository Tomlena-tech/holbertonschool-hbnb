from flask_restx import Namespace, Resource, fields
from app.services.facade import HBnBFacade


# ------------------------------------------------------------
# Initialisation de la façade et du namespace pour les routes d'avis
# ------------------------------------------------------------

facade = HBnBFacade()
api = Namespace('reviews', description='Review operations')

# ------------------------------------------------------------
# Modèle de validation et de documentation pour un avis
# ------------------------------------------------------------

review_model = api.model(
    'Review',
    {
        'text': fields.String(
            required=True,
            description='Text of the review'
        ),
        'rating': fields.Integer(
            required=True,
            description='Rating of the place (1-5)'
        ),
        'user_id': fields.String(
            required=True,
            description='ID of the user'
        ),
        'place_id': fields.String(
            required=True,
            description='ID of the place'
        ),
    }
)

# ------------------------------------------------------------


@api.route('/')
class ReviewList(Resource):

    """
    Création de la class ReviewLists qui est une enfant de
    Ressource. Cette class s'occupe de gérer la création et
    la récupération de touts les avis.
    """

    @api.expect(review_model)
    @api.response(201, 'Review successfully created')
    @api.response(400, 'Invalid input data')
    def post(self):

        """
        Méthode pour enregistrer un nouvelle avis.
        Les codes erreurs sont :
         - 201 : Succès création du nouvelle avis
         - 400 : Erreur dans les valeurs donner par
         l'utilisateur.
        """

        review_data = api.payload
        new_review = facade.create_review(review_data)
        return {
            'id': new_review.id,
            'text': new_review.text,
            'rating': new_review.rating,
            'user_id': new_review.user.id,  # ✅ CORRIGÉ
            'place_id': new_review.place.id,  # ✅ CORRIGÉ
            'created_at': getattr(new_review, 'created_at', None)
        }, 201

# ------------------------------------------------------------

    @api.response(200, 'List of reviews retrieved successfully')
    def get(self):

        """
        Méthode pour récupérer une listes d'avis.
        Les codes erreurs sont :
         - 201 : Succès création de la listes.
         - 400 : Erreur dans les valeurs donner par
         l'utilisateur.
        """

        reviews = facade.get_all_reviews()
        return [
            {
                'id': r.id,
                'text': r.text,
                'rating': r.rating,
                'user_id': r.user.id,  # ✅ CORRIGÉ
                'place_id': r.place.id  # ✅ CORRIGÉ
            }for r in reviews
        ], 200

# ------------------------------------------------------------


@api.route('/<review_id>')
class ReviewResource(Resource):

    """
    Création de la classe ReviewResource qui est une enfant de
    Resource.
    Cette classe permet de gérer les opérations,
    qui concerne sur un avis spécifique (GET, PUT, DELETE)
    """

    @api.response(200, 'Review details retrieved successfully')
    @api.response(404, 'Review not found')
    def get(self, review_id):

        """
        Méthodes d'instance qui permet d'obtenir
        les détails d'un avis spécifique.
        Les codes erreurs sont :
         - 201 : Succès retour du détails de l'avis.
         - 400 : Erreur l'id est introuvable l'avis n'existe pas.
        """

        review = facade.get_review(review_id)
        if not review:
            return {'error': 'Review not found'}, 404
        return {
            'id': review.id,
            'text': getattr(review, 'text', None),
            'rating': getattr(review, 'rating', None),
            'user_id': review.user.id,  # ✅ CORRIGÉ
            'place_id': review.place.id  # ✅ CORRIGÉ
        }, 200

# ------------------------------------------------------------

    @api.expect(review_model)
    @api.response(200, 'Review updated successfully')
    @api.response(404, 'Review not found')
    @api.response(400, 'Invalid input data')
    def put(self, review_id):

        """
        Méthode qui permet de mettre à jour un avis existant.
        Les codes erreurs sont :
         - 201 : Succès mise à jour de l'avis.
         - 400 : Erreur dans les valeurs donner par
         l'utilisateur.
        """

        data = api.payload

        updated_review = facade.update_review(review_id, data)
        if not updated_review:
            return {'error': 'Review not found'}, 404

        return {
            'id': updated_review.id,
            'text': updated_review.text,
            'rating': updated_review.rating,
            'user_id': updated_review.user.id,  # ✅ CORRIGÉ
            'place_id': updated_review.place.id  # ✅ CORRIGÉ
        }, 200

# ------------------------------------------------------------

    @api.response(200, 'Review deleted successfully')
    @api.response(404, 'Review not found')
    def delete(self, review_id):

        """
        Supprimer un avis.
        Les codes erreurs sont :
         - 201 : Succès suprésion de l'avis.
         - 400 : Erreur l'avis n'existe pas.
        """

        deleted = facade.delete_review(review_id)
        if not deleted:
            return {'error': 'Review not found'}, 404
        return {'message': 'Review deleted successfully'}, 200

# ------------------------------------------------------------


@api.route('/places/<place_id>/reviews')
class PlaceReviewList(Resource):
    """
    Classe pour récupérer tout les avis liés à un lieux spécifique
    """

    @api.response(200, 'List of reviews for the place retrieved successfully')
    @api.response(404, 'Place not found')
    def get(self, place_id):

        """
        Obtenir tous les avis d'un lieu spécifique.
        Les codes erreurs sont :
         - 201 : Succès suprésion de l'avis.
         - 400 : Erreur l'avis n'existe pas.
        """

        reviews = facade.get_reviews_by_place(place_id)
        return [
            {
                'id': r.id,
                'text': r.text,
                'rating': r.rating,
                'user_id': r.user.id  # ✅ CORRIGÉ
            }for r in reviews
        ], 200

# ------------------------------------------------------------
