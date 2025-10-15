import sys, os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from flask import Flask
from flask_restx import Api
from app.api.v1.users import api as users_ns

app = Flask(__name__)
api = Api(app, title='HBnB API', version='1.0')
api.add_namespace(users_ns, path='/api/users')

# ---------- AMENITIES ----------
from app.api.v1.amenities import api as amenities_ns
api.add_namespace(amenities_ns, path='/api/amenities')
