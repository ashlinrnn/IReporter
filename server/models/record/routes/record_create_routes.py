from ....routes.create_blueprint import api_v1
from .record_routes import *


api_v1.add_resource(
    RecordResource,
    '/records/me/<int:id>',
    endpoint='/records/me/<int:id>',
)
