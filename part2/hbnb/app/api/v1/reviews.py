from flask_restx import Namespace, Resource, fields
from app.services.facade import HBnBFacade

api = Namespace('reviews', description='Review operations')
facade = HBnBFacade()

# Review model for input validation
review_model = api.model('Review', {
    'text': fields.String(required=True, description='Review text'),
    'rating': fields.Integer(required=True, description='Rating from 1-5'),
    'user_id': fields.String(required=True, description='ID of the user'),
    'place_id': fields.String(required=True, description='ID of the place')
})
#------------------------------------------------------------

@api.route('/')
class ReviewList(Resource):
    #create class ReviewList(Resource): who's methods are get and post
    @api.response(200, 'List of reviews retrieved successfully')
    def get(self):
        """Retrieve all reviews"""
        reviews = facade.get_all_reviews()
        return [{
            'id': review.id,
            'text': review.text,
            'rating': review.rating,
            'place_id': review.place.id,  
            'user_id': review.user.id,    
            'created_at': review.created_at.isoformat(),
            'updated_at': review.updated_at.isoformat()
        } for review in reviews], 200

    @api.expect(review_model)
    @api.response(201, 'Review created successfully')
    @api.response(400, 'Invalid input data')
    def post(self):
        """Create a new review"""
        review_data = api.payload
        try:
            new_review = facade.create_review(review_data)
            return {
                'id': new_review.id,
                'text': new_review.text,
                'rating': new_review.rating,
                'place_id': new_review.place.id,  
                'user_id': new_review.user.id,    
                'created_at': new_review.created_at.isoformat(),
                'updated_at': new_review.updated_at.isoformat()
            }, 201
        except ValueError as e:
            return {'error': str(e)}, 400


@api.route('/<review_id>')
class ReviewResource(Resource):
    @api.response(200, 'Review details retrieved successfully')
    @api.response(404, 'Review not found')
    def get(self, review_id):
        """Get a review by ID"""
        review = facade.get_review(review_id)
        if not review:
            return {'error': 'Review not found'}, 404
        return {
            'id': review.id,
            'text': review.text,
            'rating': review.rating,
            'place_id': review.place.id,  
            'user_id': review.user.id,    
            'created_at': review.created_at.isoformat(),
            'updated_at': review.updated_at.isoformat()
        }, 200

    @api.expect(review_model)
    @api.response(200, 'Review updated successfully')
    @api.response(404, 'Review not found')
    @api.response(400, 'Invalid input data')
    def put(self, review_id):
        """Update a review"""
        review_data = api.payload
        try:
            updated_review = facade.update_review(review_id, review_data)
            if not updated_review:
                return {'error': 'Review not found'}, 404
            return {
                'id': updated_review.id,
                'text': updated_review.text,
                'rating': updated_review.rating,
                'place_id': updated_review.place.id,  
                'user_id': updated_review.user.id,    
                'created_at': updated_review.created_at.isoformat(),
                'updated_at': updated_review.updated_at.isoformat()
            }, 200
        except ValueError as e:
            return {'error': str(e)}, 400

    @api.response(200, 'Review deleted successfully')
    @api.response(404, 'Review not found')
    def delete(self, review_id):
        """Delete a review"""
        success = facade.delete_review(review_id)
        if not success:
            return {'error': 'Review not found'}, 404
        return {'message': 'Review deleted successfully'}, 200
    