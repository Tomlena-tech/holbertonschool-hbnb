from flask_restx import Namespace, Resource, fields
from models.amenity import Amenity

api = Namespace('amenities', description='Amenity operations')

amenity_model = api.model('Amenity', {
    'name': fields.String(required=True, description='Amenity name (max 50)')
})

AMENITIES = {}   # stock volatile


@api.route('/')
class AmenityList(Resource):
    @api.response(200, 'List of amenities retrieved')
    def get(self):
        return [a.to_dict() for a in AMENITIES.values()], 200

    @api.expect(amenity_model, validate=True)
    @api.response(201, 'Amenity successfully created')
    def post(self):
        data = api.payload
        try:
            amenity = Amenity(name=data['name'])
        except (TypeError, ValueError) as e:
            return {'error': str(e)}, 400
        AMENITIES[amenity.id] = amenity
        return amenity.to_dict(), 201
