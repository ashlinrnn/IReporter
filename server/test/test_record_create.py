
import pytest
from server.app import create_app
from server.config import db
from server.models import User, Record
from server.utils.auth import create_token

@pytest.fixture(scope='module')
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

def create_user_and_token(is_admin=False):
    user = User(
        username='testuser',
        email='test@example.com',
        password='password123',
        is_admin=is_admin
    )
    db.session.add(user)
    db.session.commit()
    token = create_token(user.id)
    return user, token

def test_create_record_success(client):
    """Authenticated user can create a record via /records/create."""
    user, token = create_user_and_token()
    headers = {'Authorization': f'Bearer {token}'}
    data = {
        'title': 'Bad road section',
        'description': 'Potholes on Kenyatta Avenue',
        'type': 'intervention',
        'latitude': -1.286389,
        'longitude': 36.817223
    }
    response = client.post('/api/v1/records/create', json=data, headers=headers)
    assert response.status_code == 201
    resp_json = response.json
    assert 'data' in resp_json
    record = resp_json['data']
    assert record['title'] == data['title']
    assert record['description'] == data['description']
    assert record['type'] == data['type']
    assert record['latitude'] == data['latitude']
    assert record['longitude'] == data['longitude']
    assert record['user_id'] == user.id
    assert record['status'] == 'pending'

# def test_create_record_missing_fields(client):
#     """Missing required fields return 400."""
#     user, token = create_user_and_token()
#     headers = {'Authorization': f'Bearer {token}'}
    
#     response = client.post('/api/v1/records/create', json={'title': 'Bad road', 'type': 'intervention'}, headers=headers)
#     assert response.status_code == 400
    # assert 'message' in response.json

def test_create_record_unauthenticated(client):
    """Request without token returns 401."""
    response = client.post('/api/v1/records/create', json={'title': 'test', 'description': 'desc', 'type': 'red flag'})
    assert response.status_code == 401

def test_create_record_invalid_type(client):
    """Invalid record type returns 400 (validation error)."""
    user, token = create_user_and_token()
    headers = {'Authorization': f'Bearer {token}'}
    data = {
        'title': 'Test',
        'description': 'Description',
        'type': 'invalid_type'
    }
    response = client.post('/api/v1/records/create', json=data, headers=headers)
    assert response.status_code == 400