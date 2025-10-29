from flask_restx import Api

# ----------  imports des namespaces ----------
from app.api.v1.users      import api as users_ns
from app.api.v1.reviews    import api as reviews_ns
from app.api.v1.places     import api as places_ns
from app.api.v1.amenities  import api as amenities_ns
from app.api.v1.auth       import api as auth_ns

# ----------  instance unique ----------
api_v1 = Api(
    version='1.0',
    title='HBnB API',
    description='HBnB Application API',
    doc='/api/v1/doc'
)

# ----------  enregistrement ----------
api_v1.add_namespace(users_ns,      path='/api/v1/users')
api_v1.add_namespace(reviews_ns,    path='/api/v1/reviews')
api_v1.add_namespace(places_ns,     path='/api/v1/places')
api_v1.add_namespace(amenities_ns,  path='/api/v1/amenities')
api_v1.add_namespace(auth_ns,       path='/api/v1/auth')
