# server/blueprints/auth.py (or similar)
from flask_restful import Resource
from flask import request, g, current_app
from ....utils.auth import create_token, login_required
from ....models import User
from ....config import db
import jwt
from datetime import datetime, timedelta
from ....services.email_service import send_password_reset_email

class SignupResource(Resource):
    def post(self):
        data = request.get_json()
        username = data.get('username', '').strip().lower() 
        email = data.get('email', '').strip().lower()       
        password = data.get('password')

        if not username or not email or not password:
            return {'message': 'Username, email, and password are required'}, 400

        if User.query.filter_by(username=username).first():
            return {'message': 'Username already exists'}, 400
        if User.query.filter_by(email=email).first():
            return {'message': 'Email already exists'}, 400

        user = User(username=username, email=email, password=password)
        db.session.add(user)
        db.session.commit()

        token = create_token(user.id)
        return {'token': token, 'user': user.to_dict()}, 201

class LoginResource(Resource):
    def post(self):
        try:
            data = request.get_json()
            email = data.get('email', '').strip().lower()
            password = data.get('password')
            user = User.query.filter_by(email=email).first()
            if not user or not user.authenticate(password):
                return {'message': 'Invalid credentials'}, 401
            token = create_token(user.id)
            return {'token': token, 'user': user.to_dict()}, 200
        except Exception as e:
            import traceback
            traceback.print_exc()
            return {'message': str(e), 'trace': traceback.format_exc()}, 500
class LogoutResource(Resource):
    @login_required
    def post(self):
        # For JWT stored on client, "logout" is purely client‑side.
        return {'message': 'Logged out'}, 200
    
class CurrentUserResource(Resource):
    @login_required
    def get(self):
        # g.current_user is set by @login_required --remember
        return {'user': g.current_user.to_dict()}, 200
    
class ForgotPasswordResource(Resource):
    def post(self):
        data=request.get_json()
        email=data.get('email','').strip().lower()
        
        if not email:
            return {'message':'Email is required'}, 400
        
        user=User.query.filter_by(email=email).first()
        
        if not user:
            return {'message': 'If your email is registered, you will receive a reset link'},200
        
        reset_token=jwt.encode(
            {'user_id':user.id,'exp':datetime.utcnow()+timedelta(hours=1)},
            current_app.config['SECRET_KEY'],
            algorithm='HS256'
        )
        
        url=current_app.config.get('FRONTEND_URL')
        
        reset_link=f"{url}/forgot-password?token={reset_token}"
        
        send_password_reset_email(user.email,user.username,reset_link)
        
        return {'message':'If your email is registered, you will receive a reset link'},200
    
class ResetPasswordResource(Resource):
    def post(self):
        
        data = request.get_json()
        token = data.get('token')
        new_password = data.get('new_password')
        
        if not token or not new_password:
            return {'message': 'Token and new password are required'}, 400
        
        try:
            payload = jwt.decode(token, current_app.config['SECRET_KEY'], algorithms=['HS256'])
            user_id = payload.get('user_id')
            if not user_id:
                raise jwt.InvalidTokenError
        except jwt.InvalidTokenError:
            return {'message': 'Invalid or expired token'}, 400
        
        user = db.session.get(User, user_id)
        if not user:
            return {'message': 'User not found'}, 404
        
        user.password = new_password
        db.session.commit()
        
        return {'message': 'Password updated successfully'}, 200