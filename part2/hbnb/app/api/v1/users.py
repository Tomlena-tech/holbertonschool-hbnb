#!/usr/bin/python3
"""User API endpoints"""
from flask_restx import Namespace, Resource, fields
from app.services import facade

api = Namespace('users', description='User operations')

# Modèle d'entrée (POST + PUT)
user_model = api.model('User', {
    'first_name': fields.String(required=True, description='First name of the user'),
    'last_name':  fields.String(required=True, description='Last name of the user'),
    'email':      fields.String(required=True, description='Email of the user')
})


# ---------- LISTE + CREATION ----------
@api.route('/')
class UserList(Resource):
    @api.response(200, 'List of users retrieved successfully')
    def get(self):
        """Retrieve the list of users"""
        users = facade.get_all_users()
        return [
            {
                'id': u.id,
                'first_name': u.first_name,
                'last_name':  u.last_name,
                'email':      u.email
            } for u in users
        ], 200

    @api.expect(user_model, validate=True)
    @api.response(201, 'User successfully created')
    @api.response(400, 'Email already registered or invalid input data')
    def post(self):
        """Register a new user"""
        user_data = api.payload
        
        # Vérification email unique
        existing_user = facade.get_user_by_email(user_data['email'])
        if existing_user:
            return {'error': 'Email already registered'}, 400
        
        # Création avec gestion d'erreurs
        try:
            new_user = facade.create_user(user_data)
            return {
                'id': new_user.id,
                'first_name': new_user.first_name,
                'last_name':  new_user.last_name,
                'email':      new_user.email
            }, 201
        except (TypeError, ValueError) as e:
            return {'error': str(e)}, 400


# ---------- GET by ID + PUT ----------
@api.route('/<user_id>')
class UserResource(Resource):
    @api.response(200, 'User details retrieved successfully')
    @api.response(404, 'User not found')
    def get(self, user_id):
        """Get user details by ID"""
        user = facade.get_user(user_id)
        if not user:
            return {'error': 'User not found'}, 404
        return {
            'id': user.id,
            'first_name': user.first_name,
            'last_name':  user.last_name,
            'email':      user.email
        }, 200

    @api.expect(user_model, validate=True)
    @api.response(200, 'User updated successfully')
    @api.response(404, 'User not found')
    @api.response(400, 'Invalid input data or email already registered')
    def put(self, user_id):
        """Update user information"""
        user_data = api.payload
        
        # Vérifier que l'utilisateur existe
        user = facade.get_user(user_id)
        if not user:
            return {'error': 'User not found'}, 404
        
        # Si l'email change, vérifier qu'il n'existe pas déjà
        if 'email' in user_data and user_data['email'] != user.email:
            existing = facade.get_user_by_email(user_data['email'])
            if existing:
                return {'error': 'Email already registered'}, 400
        
        # Mise à jour avec gestion d'erreurs
        try:
            updated_user = facade.update_user(user_id, user_data)
            return {
                'id': updated_user.id,
                'first_name': updated_user.first_name,
                'last_name':  updated_user.last_name,
                'email':      updated_user.email
            }, 200
        except (TypeError, ValueError) as e:
            return {'error': str(e)}, 400
        