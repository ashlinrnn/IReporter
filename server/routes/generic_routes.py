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
            f'{endpoint}/<int:id>',
            endpoint=f'{endpoint}/<int:id>',
            resource_class_args=(model,resource,rules)
        )
    except Exception as e:
        print(f'❌failed to create routes for {resource}',str(e))
    finally: 
        print(f'✅created routes {resource}')
