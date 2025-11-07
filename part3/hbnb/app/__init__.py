from flask import Flask
from flask_restx import Api
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager
from flask_bcrypt import Bcrypt

db = SQLAlchemy()
jwt = JWTManager()
bcrypt = Bcrypt()

from app.api.v1.users import api as users_ns
from app.api.v1.amenities import api as amenities_ns
from app.api.v1.places import api as places_ns
from app.api.v1.reviews import api as reviews_ns
from app.api.v1.auth import api as auth_ns 

def create_app(config_class='config.DevelopmentConfig'):
    app = Flask(__name__)
    app.config['SERVER_NAME'] = None
    app.config['APPLICATION_ROOT'] = '/'
    app.config['PREFERRED_URL_SCHEME'] = 'https'
    app.config.from_object(config_class)
    db.init_app(app)
    jwt.init_app(app)
    bcrypt.init_app(app)
    
    from flask import jsonify
    @app.route('/')
    def index():
        return jsonify({
            "message": "HBnB API is running",
            "swagger": "/api/v1/docs",
            "version": "1.0"
        }), 200
    
    api = Api(app, version='1.0', title='HBnB API', description='HBnB Application API', doc='/api/v1/docs')

    # Register the users namespace
    api.add_namespace(users_ns, path='/api/v1/users')
    # Register the amenities namespace
    api.add_namespace(amenities_ns, path='/api/v1/amenities')
    # Register the places namespace
    api.add_namespace(places_ns, path='/api/v1/places')
    # Register the reviews namespace
    api.add_namespace(reviews_ns, path='/api/v1/reviews')
    # Register the auth namespace
    api.add_namespace(auth_ns, path='/api/v1/auth') 
    
    
    with app.app_context():
        db.create_all()
    
    return app
