#!/usr/bin/python3
from flask_restx import Namespace, Resource, fields
from app.services.facade import facade

api = Namespace('amenities', description='Amenity operations')

amenity_in = api.model('AmenityInput', {
    'name': fields.String(required=True, description='Amenity name (max 50)')
})

AMENITIES = {}   # stock volatile


@api.route('/')
class AmenityList(Resource):
    @api.response(200, 'List of amenities retrieved')
    def get(self):
        return [a.to_dict() for a in AMENITIES.values()], 200

    @api.expect(amenity_in, validate=True)
    @api.response(201, 'Amenity successfully created')
    def post(self):
        data = api.payload
        try:
            amenity = facade.create_amenity(data)
            return amenity.to_dict(), 201
        except ValueError as e:
            return {'error': str(e)}, 400
