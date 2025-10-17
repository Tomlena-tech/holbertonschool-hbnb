from flask_restx import Namespace, Resource, fields
from app.services.facade import HBnBFacade

api = Namespace('places', description='Place operations')
facade = HBnBFacade()

# Place model for input validation
place_model = api.model('Place', {
    'title': fields.String(required=True, description='Place title'),
    'description': fields.String(description='Place description'),
    'price': fields.Float(required=True, description='Price per night'),
    'latitude': fields.Float(required=True, description='Latitude'),
    'longitude': fields.Float(required=True, description='Longitude'),
    'owner_id': fields.String(required=True, description='Owner user ID')
})


@api.route('/')
class PlaceList(Resource):
    @api.response(200, 'List of places retrieved successfully')
    def get(self):
        """Retrieve all places"""
        places = facade.get_all_places()
        return [{
            'id': place.id,
            'title': place.title,
            'description': place.description,
            'price': place.price,
            'latitude': place.latitude,
            'longitude': place.longitude,
            'owner_id': place.owner.id,  
            'created_at': place.created_at.isoformat(),
            'updated_at': place.updated_at.isoformat()
        } for place in places], 200

    @api.expect(place_model)
    @api.response(201, 'Place created successfully')
    @api.response(400, 'Invalid input data')
    def post(self):
        """Create a new place"""
        place_data = api.payload
        try:
            new_place = facade.create_place(place_data)
            return {
                'id': new_place.id,
                'title': new_place.title,
                'description': new_place.description,
                'price': new_place.price,
                'latitude': new_place.latitude,
                'longitude': new_place.longitude,
                'owner_id': new_place.owner.id,  
                'amenities': new_place.amenities,
                'created_at': new_place.created_at.isoformat(),
                'updated_at': new_place.updated_at.isoformat()
            }, 201
        except ValueError as e:
            return {'error': str(e)}, 400


@api.route('/<place_id>')
class PlaceResource(Resource):
    @api.response(200, 'Place details retrieved successfully')
    @api.response(404, 'Place not found')
    def get(self, place_id):
        """Get a place by ID"""
        place = facade.get_place(place_id)
        if not place:
            return {'error': 'Place not found'}, 404
        return {
            'id': place.id,
            'title': place.title,
            'description': place.description,
            'price': place.price,
            'latitude': place.latitude,
            'longitude': place.longitude,
            'owner_id': place.owner.id,  
            'amenities': place.amenities,
            'created_at': place.created_at.isoformat(),
            'updated_at': place.updated_at.isoformat()
        }, 200

    @api.expect(place_model)
    @api.response(200, 'Place updated successfully')
    @api.response(404, 'Place not found')
    @api.response(400, 'Invalid input data')
    def put(self, place_id):
        """Update a place"""
        place_data = api.payload
        try:
            updated_place = facade.update_place(place_id, place_data)
            if not updated_place:
                return {'error': 'Place not found'}, 404
            return {
                'id': updated_place.id,
                'title': updated_place.title,
                'description': updated_place.description,
                'price': updated_place.price,
                'latitude': updated_place.latitude,
                'longitude': updated_place.longitude,
                'owner_id': updated_place.owner.id,  
                'amenities': updated_place.amenities,
                'created_at': updated_place.created_at.isoformat(),
                'updated_at': updated_place.updated_at.isoformat()
            }, 200
        except ValueError as e:
            return {'error': str(e)}, 400
        