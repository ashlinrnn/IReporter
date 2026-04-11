
import pytest
from unittest.mock import patch
from datetime import datetime, timedelta
import jwt
from server.app import create_app
from server.config import db
from server.models import User, PasswordReset

@pytest.fixture(scope='module')
def app():
    test_config = {
        'TESTING': True,
        'SQLALCHEMY_DATABASE_URI': 'sqlite:///:memory:',
        'SECRET_KEY': 'test-secret-key-32-chars!!',
        'FRONTEND_URL': 'http://localhost:5173'
    }
    app = create_app(test_config)
    return app

@pytest.fixture
def client(app):
    with app.app_context():
        db.create_all()
        yield app.test_client()
        db.session.remove()
        db.drop_all()

def create_user(email='test@example.com', password='oldpassword'):
    user = User(
        username='testuser',
        email=email,
        password=password,
        is_admin=False
    )
    db.session.add(user)
    db.session.commit()
    return user


@patch('server.models.user.routes.user_routes.send_password_reset_code_email')
def test_forgot_password_valid_email(mock_send_email, client):
    user = create_user()
    response = client.post('/api/v1/auth/forgot-password', json={'email': user.email})
    assert response.status_code == 200
    assert 'If your email is registered' in response.json['message']
    mock_send_email.assert_called_once()
    args, _ = mock_send_email.call_args
    assert args[0] == user.email
    assert args[1] == user.username
    
    reset_record = PasswordReset.query.filter_by(email=user.email).first()
    assert reset_record is not None
    assert len(reset_record.code) == 6
    assert reset_record.code == args[2]  

def test_forgot_password_unregistered_email(client):
    with patch('server.services.email_service.send_password_reset_code_email') as mock_send:
        response = client.post('/api/v1/auth/forgot-password', json={'email': 'nonexistent@example.com'})
        assert response.status_code == 200
        assert 'If your email is registered' in response.json['message']
        mock_send.assert_not_called()
        
        assert PasswordReset.query.count() == 0

def test_forgot_password_missing_email(client):
    response = client.post('/api/v1/auth/forgot-password', json={})
    assert response.status_code == 400
    assert 'Email is required' in response.json['message']


def test_verify_reset_code_valid(client,app):
    user = create_user()
    
    code = PasswordReset.create_reset_code(user.email)
    response = client.post('/api/v1/auth/verify-reset-code', json={
        'email': user.email,
        'code': code
    })
    assert response.status_code == 200
    assert 'reset_token' in response.json
    
    assert PasswordReset.query.filter_by(email=user.email).first() is None
    
    token = response.json['reset_token']
    payload = jwt.decode(token, app.config['SECRET_KEY'], algorithms=['HS256'])
    assert payload['email'] == user.email

def test_verify_reset_code_invalid_code(client):
    user = create_user()
    
    PasswordReset.create_reset_code(user.email)
    response = client.post('/api/v1/auth/verify-reset-code', json={
        'email': user.email,
        'code': '999999'
    })
    assert response.status_code == 400
    assert 'Invalid or expired code' in response.json['message']
    
    assert PasswordReset.query.filter_by(email=user.email).first() is not None

def test_verify_reset_code_expired(client):
    user = create_user()
    
    from datetime import datetime, timedelta
    reset = PasswordReset(email=user.email, code='123456', expires_at=datetime.utcnow() - timedelta(minutes=1))
    db.session.add(reset)
    db.session.commit()
    response = client.post('/api/v1/auth/verify-reset-code', json={
        'email': user.email,
        'code': '123456'
    })
    assert response.status_code == 400
    assert 'Invalid or expired code' in response.json['message']

def test_verify_reset_code_missing_fields(client):
    response = client.post('/api/v1/auth/verify-reset-code', json={'email': 'a@b.com'})
    assert response.status_code == 400
    assert 'Email and code are required' in response.json['message']


def test_reset_password_with_valid_token(client, app):
    user = create_user()
    
    reset_token = jwt.encode(
        {'email': user.email, 'exp': datetime.utcnow() + timedelta(minutes=10)},
        app.config['SECRET_KEY'],
        algorithm='HS256'
    )
    new_password = 'newSecurePass123'
    response = client.post('/api/v1/auth/reset-password', json={
        'email': user.email,
        'reset_token': reset_token,
        'password': new_password
    })
    assert response.status_code == 200
    assert response.json['message'] == 'Password updated successfully'
    db.session.refresh(user)
    assert user.authenticate(new_password) is True
    assert user.authenticate('oldpassword') is False

def test_reset_password_expired_token(client, app):
    user = create_user()
    expired_token = jwt.encode(
        {'email': user.email, 'exp': datetime.utcnow() - timedelta(minutes=1)},
        app.config['SECRET_KEY'],
        algorithm='HS256'
    )
    response = client.post('/api/v1/auth/reset-password', json={
        'email': user.email,
        'reset_token': expired_token,
        'password': 'newpass'
    })
    assert response.status_code == 400
    assert 'Invalid or expired reset token' in response.json['message']

def test_reset_password_wrong_email_in_token(client, app):
    user = create_user()
    token = jwt.encode(
        {'email': 'wrong@example.com', 'exp': datetime.utcnow() + timedelta(minutes=10)},
        app.config['SECRET_KEY'],
        algorithm='HS256'
    )
    response = client.post('/api/v1/auth/reset-password', json={
        'email': user.email,
        'reset_token': token,
        'password': 'newpass'
    })
    assert response.status_code == 400
    assert 'Invalid reset token' in response.json['message']

def test_reset_password_missing_fields(client):
    response = client.post('/api/v1/auth/reset-password', json={'email': 'a@b.com'})
    assert response.status_code == 400
    assert 'Email, reset token, and new password are required' in response.json['message']

def test_reset_password_weak_password(client, app):
    user = create_user()
    reset_token = jwt.encode(
        {'email': user.email, 'exp': datetime.utcnow() + timedelta(minutes=10)},
        app.config['SECRET_KEY'],
        algorithm='HS256'
    )
    
    response = client.post('/api/v1/auth/reset-password', json={
        'email': user.email,
        'reset_token': reset_token,
        'password': '123'
    })
    assert response.status_code == 200  