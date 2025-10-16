#!/usr/bin/python3
from flask_restx import Namespace, Resource, fields
from app.services.facade import HBnBFacade

api = Namespace('reviews', description='Review operations')
facade = HBnBFacade()
review_model = api.model('Review', {
    'text':     fields.String(required=True, description='Review text'),
    'rating':   fields.Integer(required=True, description='Rating 1-5'),
    'place_id': fields.String(required=True, description='Place ID'),
    'user_id':  fields.String(required=True, description='User ID')
})


@api.route('/')
class ReviewList(Resource):
    def post(self):
        reviews = facade.get_all_reviews()
        return [{
            'id': review.id,
            'text': review.text,
            'rating': review.rating,
            'place_id': review.place_id,
            'user_id': review.user_id,
            'created_at': review.created_at.isoformat(),
            'updated_at': review.updated_at.isoformat()
        } for review in reviews], 200
    
    @api.response(200, 'List of reviews retrieved')
    @api.expect(review_model, validate=True)
    @api.response(201, 'Review successfully created')
    @api.response(400, 'Invalid input data')
    def post(self):
        """Create a new review"""
        review_data = api.payload
        new_review = facade.create(review_data)
        return {
             'id': new_review.id,
                'text': new_review.text,
                'rating': new_review.rating,
                'place_id': new_review.place_id,
                'user_id': new_review.user_id,
                'created_at': new_review.created_at.isoformat(),
                'updated_at': new_review.updated_at.isoformat()
            }, 201
    
    @api.response (200, 'List of reviews retrieved successfully')
    def get(self):
        """Retrieve all reviews"""
        reviews = facade.get_all_reviews()
        return [{
            'id': review.id,
            'text': review.text,
            'rating': review.rating,
            'place_id': review.place_id,
            'user_id': review.user_id,
            'created_at': review.created_at.isoformat(),
            'updated_at': review.updated_at.isoformat()
        } for review in reviews], 200
        
    @api.route('/<string:review_id>')
    class ReviewResource(Resource):
        
        @api.response(200, 'Review retrieved successfully')
        @api.response(404, 'Review not found')
        def get(self, review_id):
            """Retrieve a specific review by ID"""
            review = facade.get_review_by_id(review_id)
            if not review:
                return {'error': 'Review not found'}, 404
            return {
                'id': review.id,
                'text': review.text,
                'rating': review.rating,
                'place_id': review.place_id,
                'user_id': review.user_id,
                'created_at': review.created_at.isoformat(),
                'updated_at': review.updated_at.isoformat()
            }, 200
            
#----------------------------------------------------            
        @api.expect(review_model, validate=True)
        @api.response(200, 'Review updated successfully')
        @api.response(400, 'Invalid input data')
        @api.response(404, 'Review not found')
        def put(self, review_id):
            """Update a specific review by ID"""
            review_data = api.payload
            updated_review = facade.update_review(review_id, review_data)
            if not updated_review:
                return {'error': 'Review not found'}, 404
            return {
                'id': updated_review.id,
                'text': updated_review.text,
                'rating': updated_review.rating,
                'place_id': updated_review.place_id,
                'user_id': updated_review.user_id,
                'created_at': updated_review.created_at.isoformat(),
                'updated_at': updated_review.updated_at.isoformat()
            }, 200
            
#----------------------------------------------------            

        @api.response(200, 'Review deleted successfully')
        @api.response(404, 'Review not found')
        def delete(self, review_id):
            """Delete a specific review by ID"""
            success = facade.delete_review(review_id)
            if not success:
                return {'error': 'Review not found'}, 404
            return {'message': 'Review deleted successfully'}, 200
    
#----------------------------------------------------

    @api.route('/places/<place_id>/reviews')
    class PlaceReviewList(Resource):
        @api.response(200, 'List of reviews for the place')
        @api.response(404, 'Place not found')
        def get(self, place_id):
            """Get all reviews for a specific place"""
            place = facade.get_place(place_id)
            if not place:
                return {'error': 'Place not found'}, 404
        
            reviews = facade.get_reviews_by_place(place_id)
            return [{
                'id': review.id,
                'text': review.text,
                'rating': review.rating,
                'user_id': review.user_id,
                'created_at': review.created_at.isoformat(),
                'updated_at': review.updated_at.isoformat()
            }  for review in reviews], 200
