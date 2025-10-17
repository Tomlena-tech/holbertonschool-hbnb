from flask_restx import Namespace, Resource, fields
from app.services import facade


# File: amenities.py
# Description:
#   This file contains the API endpoints
#   related to amenity management.
#   It allows to:
#     - Create a new amenity (POST)
#     - List all amenities (GET)
#     - View a specific amenity (GET /<amenity_id>)
#     - Update an existing amenity (PUT)

api = Namespace('amenities', description='Amenity operations')

# Define the amenity model for input validation and documentation
amenity_model = api.model('Amenity', {
    'name': fields.String(required=True, description='Name of the amenity')
})

@api.route('/')
class AmenityList(Resource):
    @api.expect(amenity_model)
    @api.response(201, 'Amenity successfully created')
    @api.response(400, 'Invalid input data')
    def post(self):
        """Register a new amenity"""
        try:
            amenity_data = api.payload
            new_amenity = facade.create_amenity(amenity_data)
            return {
                'id': new_amenity.id,
                'name': new_amenity.name,
                'created_at': new_amenity.created_at.isoformat(),
                'updated_at': new_amenity.updated_at.isoformat()
            }, 201
        except ValueError as e:
            return {'error': str(e)}, 400
        
# ------------------------------------------------------------

    @api.response(200, 'List of amenities retrieved successfully')
    def get(self):
        """Retrieve a list of all amenities"""
        amenities = facade.get_all_amenities()
        return [{
            'id': amenity.id,
            'name': amenity.name,
            'created_at': amenity.created_at.isoformat(),
            'updated_at': amenity.updated_at.isoformat()
        } for amenity in amenities], 200
        
 # ------------------------------------------------------------
   
@api.route('/<amenity_id>')
class AmenityResource(Resource):
    @api.response(200, 'Amenity details retrieved successfully')
    @api.response(404, 'Amenity not found')
    def get(self, amenity_id):
        #get amenity details by id
        """Get amenity details by ID"""
        amenity = facade.get_amenity(amenity_id)
        if not amenity:
            return {'error': 'Amenity not found'}, 404
        return {
            'id': amenity.id,
            'name': amenity.name,
            'created_at': amenity.created_at.isoformat(),
            'updated_at': amenity.updated_at.isoformat()
        }, 200
# ------------------------------------------------------------

    @api.expect(amenity_model, validate=True)
    @api.response(200, 'Amenity updated successfully')
    @api.response(404, 'Amenity not found')
    @api.response(400, 'Invalid input data')
    def put(self, amenity_id):
        """Update an amenity's information"""
        try:
            amenity_data = api.payload
            update_amenity = facade.update_amenity(amenity_id, amenity_data)
            if not update_amenity:
                return {'error': 'Amenity not found'}, 404
            return {
                'id': update_amenity.id,
                'name': update_amenity.name,
                'created_at': update_amenity.created_at.isoformat(),
                'updated_at': update_amenity.updated_at.isoformat()
            }, 200
        except ValueError as e:
            return {'error': str(e)}, 400
        