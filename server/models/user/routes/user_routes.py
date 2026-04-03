# server/blueprints/auth.py (or similar)
from flask_restful import Resource
from flask import request, g
from werkzeug.security import generate_password_hash, check_password_hash
from ....utils.auth import create_token, login_needed
from ....models import User
from ....config import db

class SignupResource(Resource):
    def post(self):
        data = request.get_json()
        username = data.get('username')
        email = data.get('email')
        password = data.get('password')
        if User.query.filter((User.email == email) | (User.username == username)).first():
            return {'error': 'User already exists'}, 400
        user = User(
            username=username,
            email=email,
            password_hash=generate_password_hash(password)
        )
        db.session.add(user)
        db.session.commit()
        token = create_token(user.id)
        return {'token': token, 'user': user.to_dict()}, 201

class LoginResource(Resource):
    def post(self):
        data = request.get_json()
        email = data.get('email')
        password = data.get('password')
        user = User.query.filter_by(email=email).first()
        if not user or not check_password_hash(user.password_hash, password):
            return {'error': 'Invalid credentials'}, 401
        token = create_token(user.id)
        return {'token': token, 'user': user.to_dict()}, 200

class LogoutResource(Resource):
    @login_needed
    def post(self):
        # For JWT stored on client, "logout" is purely client‑side.
        return {'message': 'Logged out'}, 200