from flask import Flask
from server.config import db
from flask_cors import CORS
from .config import config_app
from flask_migrate import Migrate
from  .models import *
from .routes.create_blueprint import api_bp 
import os 
import cloudinary 

def create_app(test_config=None):
    app=Flask(__name__)  
     
    
    if test_config:
        app.config.update(test_config)
    config_app(app) 

    

    cloudinary.config( 
        cloud_name=os.getenv("CLOUDINARY_CLOUD_NAME"), 
        api_key= os.getenv("CLOUDINARY_API_KEY"),
        api_secret=os.getenv("CLOUDINARY_API_SECRET"),
        secure=True
    )
    CORS(app, origins=[
            "http://localhost:5173", #dev
            "https://ireporter-xi.vercel.app" #prod 
        ],
        supports_credentials=True
        )
    
    app.register_blueprint(api_bp)
    
    return app 