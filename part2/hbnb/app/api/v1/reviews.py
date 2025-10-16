#!/usr/bin/python3
from flask_restx import Namespace, Resource, fields
from app.services.facade import facade

api = Namespace('reviews', description='Review operations')

review_in = api.model('ReviewInput', {
    'text':     fields.String(required=True, description='Review text'),
    'rating':   fields.Integer(required=True, description='Rating 1-5'),
    'place_id': fields.String(required=True, description='Place ID'),
    'user_id':  fields.String(required=True, description='User ID')
})


@api.route('/')
class ReviewList(Resource):
    @api.response(200, 'List of reviews retrieved')
    def get(self):
        reviews = facade.get_all_reviews()
        return [r.to_dict() for r in reviews], 200

    @api.expect(review_in, validate=True)
    @api.response(201, 'Review successfully created')
    def post(self):
        data = api.payload
        try:
            review = facade.create_review(data)
            return review.to_dict(), 201
        except ValueError as e:
            return {'error': str(e)}, 404
