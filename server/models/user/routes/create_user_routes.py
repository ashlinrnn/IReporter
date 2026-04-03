from ....routes.create_blueprint import api_v1
from .user_routes import *

api_v1.add_resource(
    LoginResource,
    '/login',
    endpoint='/login'
)

api_v1.add_resource(
    LogoutResource,
    '/logout',
    endpoint='/logout'
)

api_v1.add_resource(
    SignupResource,
    '/signup',
    endpoint='/signup'
)