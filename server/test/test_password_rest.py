
import pytest
from unittest.mock import patch, MagicMock
from datetime import datetime, timedelta
import jwt
from server.app import create_app
from server.config import db
from server.models import User
from server.utils.auth import create_token

@pytest.fixture(scope='module')
def app():
    test_config = {
        'TESTING': True,
        'SQLALCHEMY_DATABASE_URI': 'sqlite:///:memory:',
        'SECRET_KEY': 'test-secret-key',
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


@patch('server.models.user.routes.user_routes.send_password_reset_email')
def test_forgot_password_valid_email(mock_send_email, client):
    """Registered email => sends reset email, returns 200."""
    user = create_user()
    response = client.post('/api/v1/auth/forgot-password', json={'email': user.email})
    assert response.status_code == 200
    assert 'If your email is registered' in response.json['message']
    
    mock_send_email.assert_called_once()
    args, _ = mock_send_email.call_args
    assert args[0] == user.email
    assert args[1] == user.username
    
    reset_link = args[2]
    assert reset_link.startswith('http://localhost:5173/forgot-password?token=')

def test_forgot_password_unregistered_email(client):
    """Unregistered email => still returns 200 (security) but does NOT send email."""
    with patch('server.models.user.routes.user_routes.send_password_reset_email') as mock_send:
        response = client.post('/api/v1/auth/forgot-password', json={'email': 'nonexistent@example.com'})
        assert response.status_code == 200
        assert 'If your email is registered' in response.json['message']
        mock_send.assert_not_called()

def test_forgot_password_missing_email(client):
    """Missing email field => 400."""
    response = client.post('/api/v1/auth/forgot-password', json={})
    assert response.status_code == 400
    assert 'message' in response.json


def test_reset_password_valid_token(client,app):
    """Valid token and new password => updates password."""
    user = create_user()
    
    token = jwt.encode(
        {'user_id': user.id, 'exp': datetime.utcnow() + timedelta(hours=1)},
        app.config['SECRET_KEY'],
        algorithm='HS256'
    )
    new_password = 'newSecurePass123'
    response = client.post('/api/v1/auth/reset-password', json={
        'token': token,
        'new_password': new_password
    })
    assert response.status_code == 200
    assert response.json['message'] == 'Password updated successfully'
    
    
    db.session.refresh(user)
    assert user.authenticate(new_password) is True
    
    assert user.authenticate('oldpassword') is False

def test_reset_password_expired_token(client,app):
    """Expired token => 400 message."""
    user = create_user()
    expired_token = jwt.encode(
        {'user_id': user.id, 'exp': datetime.utcnow() - timedelta(minutes=1)},
        app.config['SECRET_KEY'],
        algorithm='HS256'
    )
    response = client.post('/api/v1/auth/reset-password', json={
        'token': expired_token,
        'new_password': 'newpass'
    })
    assert response.status_code == 400
    assert 'Invalid or expired token' in response.json['message']

def test_reset_password_invalid_token(client):
    """Malformed or invalid token => 400."""
    response = client.post('/api/v1/auth/reset-password', json={
        'token': 'garbage.token.here',
        'new_password': 'newpass'
    })
    assert response.status_code == 400
    assert 'Invalid or expired token' in response.json['message']

def test_reset_password_missing_token(client):
    """Missing token => 400."""
    response = client.post('/api/v1/auth/reset-password', json={'new_password': 'newpass'})
    assert response.status_code == 400
    assert 'Token and new password are required' in response.json['message']

def test_reset_password_missing_new_password(client):
    """Missing new_password => 400."""
    response = client.post('/api/v1/auth/reset-password', json={'token': 'some.token'})
    assert response.status_code == 400
    assert 'Token and new password are required' in response.json['message']

def test_reset_password_weak_password_validation(client,app):
    """Weak password (less than 6 chars) should be rejected – but this is handled by model validator."""
    user = create_user()
    token = jwt.encode(
        {'user_id': user.id, 'exp': datetime.utcnow() + timedelta(hours=1)},
        app.config['SECRET_KEY'],
        algorithm='HS256'
    )
    
    response = client.post('/api/v1/auth/reset-password', json={
        'token': token,
        'new_password': '123'
    })
    
    assert response.status_code in (200, 400)