import os
import pytest
from faker import Faker
from server.app import create_app
from server.models import User, Record
from server.config import db

# Force in‑memory database for tests
os.environ['FLASK_SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'

fake = Faker()

@pytest.fixture(scope='session')
def app():
    test_config = {
        'TESTING': True,
        'SQLALCHEMY_DATABASE_URI': 'sqlite:///:memory:',
        'SECRET_KEY': 'test-secret-key'
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

class TestRoutes:
    def test_get_users(self, client):
        # Use password= instead of password_hash=
        user1 = User(
            username='Jack Black',
            email='jackblack@gmail.com',
            password='jackblack123',      # <- fixed
        )
        user2 = User(
            username='Jack Blue',
            email='jackblue@gmail.com',
            password='jackblue123',       # <- fixed
        )
        db.session.add_all([user1, user2])
        db.session.commit()

        response = client.get('/api/v1/users')
        assert response.status_code == 200
        assert response.content_type == 'application/json'

        data = response.json
        items = data['data']
        total = data['total']
        users = User.query.all()

        # Sort to ignore order
        assert sorted(u['id'] for u in items) == sorted(u.id for u in users)
        assert sorted(u['username'] for u in items) == sorted(u.username for u in users)
        assert sorted(u['email'] for u in items) == sorted(u.email for u in users)
        assert total == len(users)

    def test_get_users_by_id(self, client):
        user = User(
            username='Jack Black',
            email='jackblack@gmail.com',
            password='jackblack123',
        )
        db.session.add(user)
        db.session.commit()

        response = client.get(f'/api/v1/users/{user.id}')
        assert response.status_code == 200
        assert response.content_type == 'application/json'

        data = response.json
        item = data['data']
        assert item['id'] == user.id
        assert item['username'] == user.username
        assert item['email'] == user.email

    def test_patch_users(self, client):
        user = User(
            username='Jack Black',
            email='jackblack@gmail.com',
            password='jackblack123',
        )
        db.session.add(user)
        db.session.commit()

        new_username = user.username + 'JBGreat'
        response = client.patch(
            f'/api/v1/users/{user.id}',
            json={'username': new_username}
        )
        assert response.status_code == 200
        assert response.content_type == 'application/json'

        data = response.json
        item = data['data']
        updated_user = db.session.get(User, user.id)
        assert item['email'] == user.email
        assert updated_user.username == new_username

    def test_delete_user(self, client):
        user = User(
            username='Jack Black',
            email='jackblack@gmail.com',
            password='jackblack123',
        )
        db.session.add(user)
        db.session.commit()

        response = client.delete(f'/api/v1/users/{user.id}')
        assert response.status_code == 204

    def test_get_records(self, client):
        user = User(
            username='testuser',
            email='test@example.com',
            password='test123',
        )
        db.session.add(user)
        db.session.commit()

        record1 = Record(
            user_id=user.id,
            type='red flag',
            title='IEBC corruption case',
            description='any description here will work',
            status='pending'
        )
        record2 = Record(
            user_id=user.id,
            type='red flag',
            title='KEMSA corruption case',
            description='any description here will work',
            status='pending'
        )
        db.session.add_all([record1, record2])
        db.session.commit()

        response = client.get('/api/v1/records')
        assert response.status_code == 200
        assert response.content_type == 'application/json'

        data = response.json
        items = data['data']
        total = data['total']
        records = Record.query.all()

        assert total == len(records)
        # Sort to avoid order mismatch (API returns newest first)
        assert sorted(r['id'] for r in items) == sorted(r.id for r in records)
        assert sorted(r['title'] for r in items) == sorted(r.title for r in records)
        assert sorted(r['type'] for r in items) == sorted(r.type for r in records)
        assert sorted(r['description'] for r in items) == sorted(r.description for r in records)
        assert sorted(r['status'] for r in items) == sorted(r.status for r in records)

    def test_get_records_by_id(self, client):
        user = User(
            username='testuser',
            email='test@example.com',
            password='test123',
        )
        db.session.add(user)
        db.session.commit()

        record = Record(
            user_id=user.id,
            type='red flag',
            title='KEMSA corruption case',
            description='any description here will work',
            status='pending'
        )
        db.session.add(record)
        db.session.commit()

        response = client.get(f'/api/v1/records/{record.id}')
        assert response.status_code == 200
        assert response.content_type == 'application/json'

        data = response.json
        item = data['data']
        assert item['id'] == record.id
        assert item['status'] == record.status
        assert item['description'] == record.description
        assert item['type'] == record.type
        assert item['title'] == record.title

    def test_patch_records(self, client):
        user = User(
            username='testuser',
            email='test@example.com',
            password='test123',
        )
        db.session.add(user)
        db.session.commit()

        record = Record(
            user_id=user.id,
            type='red flag',
            title='KEMSA corruption case',
            description='any description here will work',
            status='pending'
        )
        db.session.add(record)
        db.session.commit()

        new_title = record.title + ' updated'
        response = client.patch(
            f'/api/v1/records/{record.id}',
            json={'title': new_title}
        )
        assert response.status_code == 200
        assert response.content_type == 'application/json'

        data = response.json
        item = data['data']
        updated_record = db.session.get(Record, record.id)
        assert item['id'] == updated_record.id
        assert item['status'] == updated_record.status
        assert item['description'] == updated_record.description
        assert item['type'] == updated_record.type
        assert 'updated' in updated_record.title

    def test_delete_records(self, client):
        user = User(
            username='Jack Black',
            email='jackblack@gmail.com',
            password='jackblack123',
        )
        db.session.add(user)
        db.session.commit()

        record = Record(
            user_id=user.id,
            type='red flag',
            title='KEMSA corruption case',
            description='any description here will work',
            status='pending'
        )
        db.session.add(record)
        db.session.commit()

        response = client.delete(f'/api/v1/records/{record.id}')
        assert response.status_code == 204