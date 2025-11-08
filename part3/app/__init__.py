from flask import Flask
from flask_restx import Api
from app.extensions import bcrypt, jwt, db


def seed_admin_user(app):
    """
    Seeds an initial admin user if no admin exists in the system.

    This function checks if any admin user exists, and if not,
    creates one using credentials from the app configuration.

    Args:
        app: The Flask application instance
    """
    from app.services import facade

    # Check if any admin user already exists
    all_users = facade.get_all_users()
    admin_exists = any(user.is_admin for user in all_users)

    if not admin_exists:
        admin_data = {
            'first_name': app.config['ADMIN_FIRST_NAME'],
            'last_name': app.config['ADMIN_LAST_NAME'],
            'email': app.config['ADMIN_EMAIL'],
            'password': app.config['ADMIN_PASSWORD'],
            'is_admin': True
        }

        # Check if user with admin email already exists (but is not admin)
        existing_user = facade.get_user_by_email(admin_data['email'])
        if existing_user:
            print(f"User with email {admin_data['email']} already exists but is not admin. Skipping admin creation.")
        else:
            facade.create_user(admin_data)
            print(f"Admin user created: {admin_data['email']}")


def create_app(config_class="config.DevelopmentConfig"):
    app = Flask(__name__)
    app.config.from_object(config_class)
    api = Api(
        app,
        version='1.0',
        title='HBnB API',
        description='HBnB Application API',
        doc='/api/v1/'
    )

    """
    Initialize extensions with the Flask app:
    - bcrypt
    - jwt
    - db (SQLAlchemy)
    """
    bcrypt.init_app(app)
    app.extensions['bcrypt'] = bcrypt
    jwt.init_app(app)
    app.extensions['jwt'] = jwt
    db.init_app(app)

    # Import API namespaces here to avoid circular imports
    from app.api.v1.users import api as users_ns
    from app.api.v1.amenities import api as amenities_ns
    from app.api.v1.places import api as places_ns
    from app.api.v1.reviews import api as reviews_ns
    from app.api.v1.auth import api as auth_ns

    # Register API namespaces
    api.add_namespace(users_ns, path='/api/v1/users')
    api.add_namespace(amenities_ns, path='/api/v1/amenities')
    api.add_namespace(places_ns, path='/api/v1/places')
    api.add_namespace(reviews_ns, path='/api/v1/reviews')
    api.add_namespace(auth_ns, path='/api/v1/auth')

    # Initialize database and seed admin user
    with app.app_context():
        # Import models to register them with SQLAlchemy
        from app import models  # noqa: F401
        db.create_all()  # Create tables before seeding
        seed_admin_user(app)

    return app
