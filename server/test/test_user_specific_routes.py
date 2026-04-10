import pytest
from server.app import create_app
from server.config import db
from server.models import User
from server.utils.auth import create_token
from werkzeug.security import generate_password_hash

@pytest.fixture(scope='session')
def app():
    test_config = {
        'TESTING': True,
        'SQLALCHEMY_DATABASE_URI': 'sqlite:///:memory:',
        'SECRET_KEY': 'test-secret'
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

def create_user(is_admin=False):
    user=User(
        username='testuser',
        email='test@example.com',
        password='hashed_pw',
        is_admin=is_admin
    )
    db.session.add(user)
    db.session.commit()
    
    token=create_token(user.id)
    return user,token

def test_login_success(client):
    """valid request return 200 and a token"""
    user=create_user(False)
    
    response=client.post('/api/v1/auth/login', json={'email':'test@example.com', 'password':'hashed_pw'})
    assert response.status_code==200
    
    data=response.json
    assert 'token' in data
    assert data['user']['email']=='test@example.com'

def test_login_wrong_password(client):
    """wrong password=>401"""
    user=create_user(False)
    response=client.post('/api/v1/auth/login', json={'email':'test@example.com', 'password':'wrong_hashed_pw'})
    
    assert response.status_code==401

def test_login_nonexist_email(client):
    """=== 401"""
    
    response=client.post('/api/v1/auth/login', 
                        json={'email':'nothing@example.com', 'password':'12334444'})
    assert response.status_code==401

def test_login_missing_credentials(client):
    """miss email/password => 401"""
    response=client.post('/api/v1/auth/login',
                        json={'email':'a@123.com'})
    assert response.status_code==401

def test_signup_success(client):
    """valid 201"""
    response=client.post('/api/v1/auth/signup',
                        json={'username':'newuser','email':'new@123.com', 'password':'newpassword'})
    assert response.status_code==201
    data = response.json
    assert 'token'in data
    assert 'user' in data
    assert data['user']['username']=='newuser'
    assert data['user']['email']=='new@123.com'

def test_signup_missing_fields(client):
    """missing => 400"""
    
    response=client.post('/api/v1/auth/signup',
                        json={'username':'123user'})
    
    assert response.status_code==400
    assert 'error' in response.json
    
def test_signup_dup_email(client):
    """email existise => 400"""
    user=create_user()
    response=client.post('/api/v1/auth/signup', json={'username':'newuser123', 'email':'test@example.com', 'password':'pass123'})
    assert response.status_code==400
    assert 'already exist' in response.json.get('error','').lower()
    
def test_signup_duplicate_username(client):
    """Username already taken → 400."""
    user=create_user()
    response = client.post('/api/v1/auth/signup', json={
        'username': 'testuser',        
        'email': 'new@example.com',
        'password': 'pw'
    })
    assert response.status_code == 400
    
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
    user,token=create_user()
    headers={'Authorization': f'Bearer {token}'}
    response=client.get('/api/v1/auth/me',headers=headers)
    
    assert response.status_code==200
    
    data=response.json
    
    user_data=data.get('user')
    assert user_data.get('id')==user.id
    assert user_data.get('username')==user.username
    assert user_data.get('email')==user.email
    
    assert 'password_hash' not in user_data