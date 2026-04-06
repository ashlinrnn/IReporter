from server.routes.create_blueprint import api_v1
from .video_routes import VideoResource, VideoByID


# 👉 ALL videos (GET, POST)
api_v1.add_resource(
    VideoResource,
    '/videos'
)

# 👉 ONE video (GET, DELETE, PATCH)
api_v1.add_resource(
    VideoByID,
    '/videos/<int:id>'
)