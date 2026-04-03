import jwt
from flask import current_app,session,request, g
from ..models.user.user import User
from ..config import db
from functools import wraps
from werkzeug.exceptions import Unauthorized,Forbidden


def create_token(user_id):
    
    payload={
        'user_id':user_id
    }
    
    token=jwt.encode(payload,current_app.config['SECRET_KEY'], algorithm='HS256')
    return token

def decode_token(token):
    try:
        payload=jwt.decode(token,current_app.config['SECRET_KEY'],algorithms=['HS256'])
        return payload
    except jwt.InvalidTokenError:
        return None

def get_user_from_token(token):
    payload=decode_token(token)
    if not payload:
        return None
    
    user_id=payload.get('user_id')
    if not user_id:
        return None
    
    return db.session.get(User,user_id)

def get_current_user():
    auth_header=request.headers.get('Authorization','')
    
    if not auth_header.startswith('Bearer '):
        return None
    
    token=auth_header.split(' ')[1]
    return get_user_from_token(token)

def login_needed(f):
    
    @wraps(f)
    def decorated(*args, **kwargs):
        user=get_current_user()
        if not user:
            raise Unauthorized('Authentication required')
        
        g.current_user=user
        return f(*args,**kwargs)
    return decorated

def admin_required(f):
    @wraps(f)
    def decorator(*args,**kwargs):
        user=get_current_user()
        if not user:
            raise Unauthorized('Authentication required')
        if not user.is_admin:
            raise Forbidden('Admin privileges required')
        g.current_user=user
        return f(*args,**kwargs)
    return decorator

def is_record_owner():
    pass

def can_edit_record(record,user):
    return record.user_id==user.id and record.status=='pending'
