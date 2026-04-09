# server/blueprints/auth.py (or similar)
from flask_restful import Resource
from flask import request, g
from ....utils.auth import create_token, login_required
from ....models import User
from ....config import db

class SignupResource(Resource):
    def post(self):
        data = request.get_json()
        username = data.get('username', '').strip().lower() 
        email = data.get('email', '').strip().lower()       
        password = data.get('password')

        if not username or not email or not password:
            return {'error': 'Username, email, and password are required'}, 400

        if User.query.filter_by(username=username).first():
            return {'error': 'Username already exists'}, 400
        if User.query.filter_by(email=email).first():
            return {'error': 'Email already exists'}, 400

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
                return {'error': 'Invalid credentials'}, 401
            token = create_token(user.id)
            return {'token': token, 'user': user.to_dict()}, 200
        except Exception as e:
            import traceback
            traceback.print_exc()
            return {'error': str(e), 'trace': traceback.format_exc()}, 500
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