from flask import Flask
from server.config import db
from flask_cors import CORS
from .config import config_app
from flask_migrate import Migrate
from  .models import *
from .routes.create_blueprint import api_pb 



def create_app(test_config=None):
    app=Flask(__name__)
    if test_config:
        app.config.update(test_config)
    config_app(app)
    CORS(app, origins=[
            "http://localhost:5173", #dev
            "https://i-reporter-inky.vercel.app" #prod 
        ],
        supports_credentials=True
        )
    
    app.register_blueprint(api_pb)
    
    return app 