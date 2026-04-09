from server.routes.create_blueprint import api_v1
from server.routes.create_generic_routes import create_routes
from server.models.video.video import Video



create_routes('/videos', Video, 'video')