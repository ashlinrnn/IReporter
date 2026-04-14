import pytest
from unittest.mock import patch, MagicMock
from server.app import create_app
from server.config import db
from server.models import User
from server.utils.auth import create_token
import io

@pytest.fixture(scope='module')
def app():
    test_config = {
        'TESTING': True,
        'SQLALCHEMY_DATABASE_URI': 'sqlite:///:memory:',
        'SECRET_KEY': 'test-secret-key-32-chars!!',
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

def create_user_and_token(email='test@example.com', username='testuser', phone=None, profile_pic=None):
    user = User(
        username=username,
        email=email,
        password='password123',
        phone_number=phone,
        profile_pic_url=profile_pic
    )
    db.session.add(user)
    db.session.commit()
    token = create_token(user.id)
    return user, token


def test_get_current_user(client):
    user, token = create_user_and_token()
    headers = {'Authorization': f'Bearer {token}'}
    response = client.get('/api/v1/auth/me', headers=headers)
    assert response.status_code == 200
    data = response.json
    assert 'user' in data
    assert data['user']['id'] == user.id
    assert data['user']['email'] == user.email
    assert data['user']['username'] == user.username
    
    assert data['user'].get('phone_number') is None
    assert data['user'].get('profile_pic_url') is None

def test_get_current_user_unauthenticated(client):
    response = client.get('/api/v1/auth/me')
    assert response.status_code == 401

def test_auth_me_with_invalid_token(client):
    """===> 401"""

    headers={'Authorization':'Bearer invalid.token.here'}
    response=client.get('/api/v1/auth/me', headers=headers)
    assert response.status_code==401

def test_auth_me_without_token(client):
    """===> 401"""
    response=client.get('/api/v1/auth/me')
    
    assert response.status_code==401

def test_auth_me_with_valid_token(client):
    user,token=create_user_and_token()
    headers={'Authorization': f'Bearer {token}'}
    response=client.get('/api/v1/auth/me',headers=headers)
    
    assert response.status_code==200
    
    data=response.json
    
    user_data=data.get('user')
    assert user_data.get('id')==user.id
    assert user_data.get('username')==user.username
    assert user_data.get('email')==user.email
    
    assert 'password_hash' not in user_data


def test_update_current_user_profile(client):
    user, token = create_user_and_token()
    headers = {'Authorization': f'Bearer {token}'}
    new_data = {
        'username': 'newname',
        'email': 'new@example.com',
        'phone_number': '+254712345678',
        'profile_pic_url': 'https://example.com/pic.jpg'
    }
    response = client.patch('/api/v1/auth/me', json=new_data, headers=headers)
    assert response.status_code == 200
    data = response.json
    assert data['user']['username'] == 'newname'
    assert data['user']['email'] == 'new@example.com'
    assert data['user']['phone_number'] == '+254712345678'
    assert data['user']['profile_pic_url'] == 'https://example.com/pic.jpg'

    
    db.session.refresh(user)
    assert user.username == 'newname'
    assert user.email == 'new@example.com'
    assert user.phone_number == '+254712345678'
    assert user.profile_pic_url == 'https://example.com/pic.jpg'

def test_update_current_user_duplicate_username(client):
    user1, token1 = create_user_and_token(email='user1@test.com', username='userone')
    user2, token2 = create_user_and_token(email='user2@test.com', username='usertwo')
    headers = {'Authorization': f'Bearer {token2}'}
    response = client.patch('/api/v1/auth/me', json={'username': 'userone'}, headers=headers)
    assert response.status_code == 400
    assert 'Username already taken' in response.json['message']

def test_update_current_user_duplicate_email(client):
    user1, token1 = create_user_and_token(email='existing@test.com', username='existing')
    user2, token2 = create_user_and_token(email='user2@test.com', username='user2')
    headers = {'Authorization': f'Bearer {token2}'}
    response = client.patch('/api/v1/auth/me', json={'email': 'existing@test.com'}, headers=headers)
    assert response.status_code == 400
    assert 'Email already in use' in response.json['message']

def test_update_current_user_phone_only(client):
    user, token = create_user_and_token()
    headers = {'Authorization': f'Bearer {token}'}
    response = client.patch('/api/v1/auth/me', json={'phone_number': '+254712345678'}, headers=headers)
    assert response.status_code == 200
    assert response.json['user']['phone_number'] == '+254712345678'


@patch('server.models.user.routes.user_routes.upload_image')
def test_upload_profile_pic_success(mock_upload, client):
    mock_upload.return_value = 'https://cloudinary.com/fake-pic.jpg'
    user, token = create_user_and_token()
    headers = {'Authorization': f'Bearer {token}'}
    data = {'profile_pic': (io.BytesIO(b'fake image content'), 'test.jpg')}
    response = client.post('/api/v1/auth/me/profile-pic', data=data, content_type='multipart/form-data', headers=headers)
    assert response.status_code == 200
    assert response.json['profile_pic_url'] == 'https://cloudinary.com/fake-pic.jpg'
    db.session.refresh(user)
    assert user.profile_pic_url == 'https://cloudinary.com/fake-pic.jpg'

def test_upload_profile_pic_no_file(client):
    user, token = create_user_and_token()
    headers = {'Authorization': f'Bearer {token}'}
    response = client.post('/api/v1/auth/me/profile-pic', headers=headers)
    assert response.status_code == 400
    assert 'No file provided' in response.json['message']

def test_upload_profile_pic_empty_filename(client):
    user, token = create_user_and_token()
    headers = {'Authorization': f'Bearer {token}'}
    data = {'profile_pic': (io.BytesIO(b''), '')}
    response = client.post('/api/v1/auth/me/profile-pic', data=data, content_type='multipart/form-data', headers=headers)
    assert response.status_code == 400
    assert 'Empty filename' in response.json['message']

def test_upload_profile_pic_unauthenticated(client):
    data = {'profile_pic': (io.BytesIO(b'fake'), 'test.jpg')}
    response = client.post('/api/v1/auth/me/profile-pic', data=data, content_type='multipart/form-data')
    assert response.status_code == 401