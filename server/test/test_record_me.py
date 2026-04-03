import pytest
from server.app import create_app
from server.config import db
from server.models import User, Record
from server.utils.auth import create_token

@pytest.fixture(scope='module')
def app():
    app = create_app()
    app.config['TESTING'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
    app.config['SECRET_KEY'] = 'test-secret-key'  
    return app

@pytest.fixture
def client(app):
    with app.app_context():
        db.create_all()
        yield app.test_client()
        db.session.remove()
        db.drop_all()

def create_user_and_record(client, is_admin=False, status='pending'):
    "Helper to create a user and a record, return (user, record, token)."
    user = User(
        username='testuser',
        email='test@example.com',
        password_hash='hashed_pw',
        is_admin=is_admin
    )
    db.session.add(user)
    db.session.commit()
    
    record = Record(
        user_id=user.id,
        type='red flag',
        title='Test Title',
        description='Test Desc',
        status=status
    )
    db.session.add(record)
    db.session.commit()
    
    token = create_token(user.id)
    return user, record, token

def test_patch_record_without_token(client):
    "PATCH without Authorization header should return 401."
    response = client.patch('/api/v1/records/me/1', json={'title': 'new'})
    assert response.status_code == 401
    assert 'Authentication required' in response.get_data(as_text=True)

def test_patch_record_with_invalid_token(client):
    "PATCH with invalid token should return 401."
    headers = {'Authorization': 'Bearer invalid.token.here'}
    response = client.patch('/api/v1/records/me/1', headers=headers, json={'title': 'new'})
    assert response.status_code == 401

def test_patch_record_non_owner(client):
    "PATCH by non-owner should return 403."
    
    user1, record, token1 = create_user_and_record(client)
    
    user2 = User(username='other', email='other@example.com', password_hash='hash')
    db.session.add(user2)
    db.session.commit()
    token2 = create_token(user2.id)
    
    headers = {'Authorization': f'Bearer {token2}'}
    response = client.patch(f'/api/v1/records/me/{record.id}', headers=headers, json={'title': 'hacked'})
    assert response.status_code == 403
    assert 'Not allowed to edit this record' in response.get_data(as_text=True)

def test_patch_record_owner_pending(client):
    "PATCH by owner when status='pending' should succeed."
    user, record, token = create_user_and_record(client, status='pending')
    headers = {'Authorization': f'Bearer {token}'}
    new_title = 'Updated Title'
    response = client.patch(f'/api/v1/records/me/{record.id}', headers=headers, json={'title': new_title})
    assert response.status_code == 200
    data = response.json
    assert data['data']['title'] == new_title
    
    updated = db.session.get(Record, record.id)
    assert updated.title == new_title

def test_patch_record_owner_not_pending(client):
    "PATCH by owner when status is not pending (e.g., 'under investigation') should be forbidden."
    user, record, token = create_user_and_record(client, status='under investigation')
    headers = {'Authorization': f'Bearer {token}'}
    response = client.patch(f'/api/v1/records/me/{record.id}', headers=headers, json={'title': 'cant change'})
    assert response.status_code == 403
    assert 'Not allowed to edit this record' in response.get_data(as_text=True)

def test_delete_record_owner_pending(client):
    " DELETE by owner when pending should succeed."
    user, record, token = create_user_and_record(client, status='pending')
    headers = {'Authorization': f'Bearer {token}'}
    response = client.delete(f'/api/v1/records/me/{record.id}', headers=headers)
    assert response.status_code == 204
    
    deleted = db.session.get(Record, record.id)
    assert deleted is None

def test_delete_record_owner_not_pending(client):
    " DELETE by owner when status not pending should be forbidden."
    user, record, token = create_user_and_record(client, status='resolved')
    headers = {'Authorization': f'Bearer {token}'}
    response = client.delete(f'/api/v1/records/me/{record.id}', headers=headers)
    assert response.status_code == 403
    
    assert db.session.get(Record, record.id) is not None

def test_delete_record_non_owner(client):
    " DELETE by non-owner should return 403."
    user1, record, token1 = create_user_and_record(client)
    user2 = User(username='other', email='other@example.com', password_hash='hash')
    db.session.add(user2)
    db.session.commit()
    token2 = create_token(user2.id)
    headers = {'Authorization': f'Bearer {token2}'}
    response = client.delete(f'/api/v1/records/me/{record.id}', headers=headers)
    assert response.status_code == 403

def test_jwt_protection_on_missing_user(client):
    "Token with non-existent user ID should be rejected."
    
    fake_token = create_token(9999)
    headers = {'Authorization': f'Bearer {fake_token}'}
    response = client.patch('/api/v1/records/me/1', headers=headers, json={'title': 'x'})
    
    assert response.status_code == 401