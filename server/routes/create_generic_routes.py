from ..models import *
from .generic_routes import create_routes

#------------user-------------
create_routes('/users', User,'User')

#----------records--------
create_routes('/records', Record, 'Record')

#----------image---------
create_routes('/images',Image,'Image')

#----------video----------
create_routes('/videos', Video,'Video')