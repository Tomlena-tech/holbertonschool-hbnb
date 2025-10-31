from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager
from config import Config
from app.api.v1 import api_v1   # ← notre API unique
from app.services import facade
from app.models.user import User

db = SQLAlchemy()
jwt = JWTManager()

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    db.init_app(app)
    jwt.init_app(app)
    api_v1.init_app(app)         # ← branchement unique

    
    if not facade.get_user_by_email("admin@hbnb.com"):
        admin = User("Admin", "User", "admin@hbnb.com", "root123", True)
        facade.user_repo.add(admin)
        print("✅ Admin initialisé automatiquement :", admin.to_dict())
    
    return app

