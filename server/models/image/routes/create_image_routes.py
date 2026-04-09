from server.routes.create_blueprint import api_v1
from server.routes.create_generic_routes import create_routes
from server.models.image.image import Image


create_routes('/images', Image, 'image')