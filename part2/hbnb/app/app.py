from flask import Flask
from flask_restx import Api
from app.api.v1.users import api as users_ns

app = Flask(__name__)
api = Api(app, title='HBnB API', version='1.0')
api.add_namespace(users_ns, path='/api/users')
