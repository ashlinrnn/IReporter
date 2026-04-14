# server/blueprints/auth.py (or similar)
from flask_restful import Resource
from flask import request, g, current_app
from ....utils.auth import create_token, login_required
from ....models import User, PasswordReset
from ....config import db
import jwt
from datetime import datetime, timedelta
from ....services.email_service import send_password_reset_code_email
from sqlalchemy.exc import OperationalError, ProgrammingError

class SignupResource(Resource):
    def post(self):
        data = request.get_json()
        username = data.get('username', '').strip().lower() 
        email = data.get('email', '').strip().lower()       
        password = data.get('password')
        phone_number=data.get('phone_number')

        if not username or not email or not password:
            return {'message': 'Username, email, and password are required'}, 400

        if User.query.filter_by(username=username).first():
            return {'message': 'Username already exists'}, 400
        if User.query.filter_by(email=email).first():
            return {'message': 'Email already exists'}, 400
        
        if phone_number=='':
            phone_number=None

        user = User(username=username, email=email, password=password, phone_number=phone_number)
        try:
            db.session.add(user)
            db.session.commit()
        except OperationalError:
            return {'message': 'Database is currently unavailable'}
        except ProgrammingError:
            return {'message': 'Your request can not be handled at this time'}
        except Exception as e:
            print(f'An unexpected error occurred: {e}')
        

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
    
class RequestResetCodeResource(Resource):
    def post(self):
        data = request.get_json()
        email = data.get('email', '').strip().lower()
        if not email:
            return {'message': 'Email is required'}, 400

        user = User.query.filter_by(email=email).first()
        if user:
            code = PasswordReset.create_reset_code(email)
            send_password_reset_code_email(user.email, user.username, code)

        return {'message': 'If your email is registered, you will receive a reset code.'}, 200

class VerifyResetCodeResource(Resource):
    def post(self):
        data = request.get_json()
        email = data.get('email', '').strip().lower()
        code = data.get('code', '').strip()

        if not email or not code:
            return {'message': 'Email and code are required'}, 400

        reset = PasswordReset.query.filter_by(email=email, code=code).first()
        if not reset or reset.expires_at < datetime.utcnow():
            return {'message': 'Invalid or expired code.'}, 400

        # Delete used code so it cannot be reused
        db.session.delete(reset)
        db.session.commit()

        # Create a short‑lived JWT token for the next step
        reset_token = jwt.encode(
            {'email': email, 'exp': datetime.utcnow() + timedelta(minutes=10)},
            current_app.config['SECRET_KEY'],
            algorithm='HS256'
        )
        return {'message': 'Code verified', 'reset_token': reset_token}, 200

class ResetPasswordWithCodeResource(Resource):
    def post(self):
        data = request.get_json()
        email = data.get('email', '').strip().lower()
        reset_token = data.get('reset_token')
        new_password = data.get('password')

        if not email or not reset_token or not new_password:
            return {'message': 'Email, reset token, and new password are required'}, 400

        try:
            payload = jwt.decode(reset_token, current_app.config['SECRET_KEY'], algorithms=['HS256'])
            if payload.get('email') != email:
                return {'message': 'Invalid reset token'}, 400
        except jwt.InvalidTokenError:
            return {'message': 'Invalid or expired reset token'}, 400

        user = User.query.filter_by(email=email).first()
        if not user:
            return {'message': 'User not found'}, 404

        user.password = new_password
        db.session.commit()
        return {'message': 'Password updated successfully'}, 200