from flask import Blueprint
from flask_restful import Api
from ..services.generic_services import *

api_pb=Blueprint('api_bp',__name__)
api_v1=Api(api_pb, prefix='/api/v1')


def create_routes(endpoint,model,resource,rules=[]):
    
    try:
        api_v1.add_resource(
            AllResource,
            endpoint,
            endpoint=endpoint,
            resource_class_args=(model,resource,rules)
        )
        
        api_v1.add_resource(
            SingleResource,
            endpoint,
            endpoint=f'{endpoint}/<int:id>',
            resource_class_args=(model,resource,rules)
        )
    finally: 
        print(f'✅created routes {resource}')
