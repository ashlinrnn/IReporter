from flask import Blueprint
from flask_restful import Api

api_pb=Blueprint('api_bp',__name__)
api_v1=Api(api_pb, prefix='/api/v1')