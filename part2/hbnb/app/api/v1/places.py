#!/usr/bin/python3
"""Place API endpoints"""
from flask_restx import Namespace, Resource, fields
from app.services import facade

api = Namespace('places', description='Place operations')

# Modèle pour les amenities (dans les réponses)
amenity_model = api.model('PlaceAmenity', {
    'id': fields.String(description='Amenity ID'),
    'name': fields.String(description='Name of the amenity')
})

# Modèle pour le owner (dans les réponses)
user_model = api.model('PlaceUser', {
    'id': fields.String(description='User ID'),
    'first_name': fields.String(description='First name of the owner'),
    'last_name': fields.String(description='Last name of the owner'),
    'email': fields.String(description='Email of the owner')
})

# Modèle pour créer/modifier un place
place_model = api.model('Place', {
    'title': fields.String(required=True, description='Title of the place'),
    'description': fields.String(description='Description of the place'),
    'price': fields.Float(required=True, description='Price per night'),
    'latitude': fields.Float(required=True, description='Latitude of the place'),
    'longitude': fields.Float(required=True, description='Longitude of the place'),
    'owner_id': fields.String(required=True, description='ID of the owner'),
    'amenities': fields.List(fields.String, required=False, description="List of amenity IDs")
})


@api.route('/')
class PlaceList(Resource):
    @api.expect(place_model, validate=True)
    @api.response(201, 'Place successfully created')
    @api.response(400, 'Invalid input data')
    @api.response(404, 'Owner not found')
    def post(self):
        """Register a new place"""
        place_data = api.payload
        
        # Vérifier que le owner existe
        owner = facade.get_user(place_data['owner_id'])
        if not owner:
            return {'error': 'Owner not found'}, 404
        
        # Vérifier que les amenities existent (si fournies)
        if 'amenities' in place_data and place_data['amenities']:
            for amenity_id in place_data['amenities']:
                amenity = facade.get_amenity(amenity_id)
                if not amenity:
                    return {'error': f'Amenity {amenity_id} not found'}, 404
        
        # Créer le place avec gestion d'erreurs
        try:
            new_place = facade.create_place(place_data)
            return new_place.to_dict(), 201
        except (TypeError, ValueError) as e:
            return {'error': str(e)}, 400

    @api.response(200, 'List of places retrieved successfully')
    def get(self):
        """Retrieve a list of all places"""
        places = facade.get_all_places()
        return [place.to_dict() for place in places], 200


@api.route('/<place_id>')
class PlaceResource(Resource):
    @api.response(200, 'Place details retrieved successfully')
    @api.response(404, 'Place not found')
    def get(self, place_id):
        """Get place details by ID"""
        place = facade.get_place(place_id)
        if not place:
            return {'error': 'Place not found'}, 404
        return place.to_dict(), 200

    @api.expect(place_model, validate=True)
    @api.response(200, 'Place updated successfully')
    @api.response(404, 'Place not found')
    @api.response(400, 'Invalid input data')
    def put(self, place_id):
        """Update a place's information"""
        place_data = api.payload
        
        # Vérifier que le place existe
        place = facade.get_place(place_id)
        if not place:
            return {'error': 'Place not found'}, 404
        
        # Si owner_id change, vérifier qu'il existe
        if 'owner_id' in place_data:
            owner = facade.get_user(place_data['owner_id'])
            if not owner:
                return {'error': 'Owner not found'}, 404
        
        # Si amenities changent, vérifier qu'elles existent
        if 'amenities' in place_data and place_data['amenities']:
            for amenity_id in place_data['amenities']:
                amenity = facade.get_amenity(amenity_id)
                if not amenity:
                    return {'error': f'Amenity {amenity_id} not found'}, 404
        
        # Mise à jour avec gestion d'erreurs
        try:
            updated_place = facade.update_place(place_id, place_data)
            return updated_place.to_dict(), 200
        except (TypeError, ValueError) as e:
            return {'error': str(e)}, 400
