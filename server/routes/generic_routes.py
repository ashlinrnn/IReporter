from .create_blueprint import api_v1
from ..services.generic_services import *

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
