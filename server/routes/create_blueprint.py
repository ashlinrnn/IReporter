# create_blueprint.py

from flask import Blueprint
from flask_restful import Api

api_bp= Blueprint('api_bp', __name__)
api_v1 = Api(api_bp, prefix='/api/v1')


#  import resources AFTER api_v1 exists
from server.routes.media import UploadImage, UploadVideo
from ..models.record.routes import * #import api routes from record models 
from ..models.user.routes import * 
from server.routes import create_generic_routes





api_v1.add_resource(UploadImage, '/images/upload')
api_v1.add_resource(UploadVideo, '/videos/upload')