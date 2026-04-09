from flask import Flask
from server.config import db
from flask_cors import CORS
from .config import config_app
from flask_migrate import Migrate
from  .models import *
from .routes.create_blueprint import api_pb 



def create_app():
    app=Flask(__name__)
    config_app(app)
    app.register_blueprint(api_pb)
    # CORS(app, origins=["http://localhost:5173/"])
    # CORS(app, origins=["https://ireporter-xi.vercel.app/"])
    
    return app 