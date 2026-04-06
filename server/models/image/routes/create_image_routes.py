from server.routes.create_blueprint import api_v1
from .image_routes import ImageResource, ImageByID



api_v1.add_resource(
    ImageResource,
    '/images'
)


api_v1.add_resource(
    ImageByID,
    '/videos/<int:id>'
)