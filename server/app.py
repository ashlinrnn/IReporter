from flask import Flask
from server.config import db
from flask_cors import CORS
from .config import config_app

def create_app():
    app=Flask(__name__)
    config_app(app)
    # CORS(app, origins=["http://localhost:5173/"])
    CORS(app, origins=["https://ireporter-xi.vercel.app/"])
    
    return app