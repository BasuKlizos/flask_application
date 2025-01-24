from flask import Flask
from flask_jwt_extended import JWTManager
from flask_pymongo import PyMongo
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
# from config import Config
import os
from urllib.parse import quote_plus

class Config:
    SECRET_KEY = os.getenv("SECRET_KEY", "your-secret-key")
    JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY", "your-jwt-secret-key")
    MONGO_USERNAME = os.getenv("MONGO_USERNAME", "basudev")
    MONGO_PASSWORD = os.getenv("MONGO_PASSWORD", "UcjOArSo3yjUaP6C")
    MONGO_CLUSTER = os.getenv("MONGO_CLUSTER", "questerdb.a26wb.mongodb.net")
    MONGO_DB = os.getenv("MONGO_DB", "flask_app")
    MONGO_URI = (
        f"mongodb+srv://{quote_plus(MONGO_USERNAME)}:{quote_plus(MONGO_PASSWORD)}@{MONGO_CLUSTER}/"
        f"{MONGO_DB}?retryWrites=true&w=majority"
    )

mongo = PyMongo()
jwt = JWTManager()
limiter = Limiter(get_remote_address)



def create_app():
    app = Flask(__name__)
    
    # Configuration
    app.config.from_object(Config)
    
    
    mongo.init_app(app)
    jwt.init_app(app)
    limiter.init_app(app)
    
    
    # Register blueprints
    from .routes.auth import auth_blueprint
    from .routes.users import users_blueprint
    app.register_blueprint(auth_blueprint)
    app.register_blueprint(users_blueprint)
    
    return app