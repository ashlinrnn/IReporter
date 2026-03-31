import pytest
from faker import Faker
from server.app import create_app
from server.models import User, Record
from server.config import db

fake = Faker()

@pytest.fixture(scope='session')
def app():
    """Create a Flask app instance for testing"""
    app = create_app()
    app.config['TESTING'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
    
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    return app

@pytest.fixture
def client(app):
    """Create a test client and set up the database for each test"""
    with app.app_context():
        db.create_all()          
        yield app.test_client()  
        db.session.remove()
        db.drop_all()            

class TestRoutes:
    
    def test_get_users(self, client):
        
        user1 = User(
            username='Jack Black',
            email='jackblack@gmail.com',
            password_hash='jackblack123',
        )
        user2 = User(
            username='Jack Blue',
            email='jackblue@gmail.com',
            password_hash='jackblue123',
        )
        db.session.add_all([user1, user2])
        db.session.commit()
        
        response = client.get('/api/v1/users')
        assert response.status_code == 200
        assert response.content_type == 'application/json'
        
        data_updated = response.json
        items=data_updated['data']
        total=data_updated['total']
        
        users = User.query.all()
        
        assert [u['id'] for u in items] == [u.id for u in users]
        assert [u['username'] for u in items] == [u.username for u in users]
        assert [u['email'] for u in items] == [u.email for u in users]
        assert total 
    
    def test_get_users_by_id(self, client):
        user = User(
            username='Jack Black',
            email='jackblack@gmail.com',
            password_hash='jackblack123',
        )
        db.session.add(user)
        db.session.commit()
        
        response = client.get(f'/api/v1/users/{user.id}')
        assert response.status_code == 200
        assert response.content_type == 'application/json'
        
        data_updated = response.json
        items=data_updated['data']
        
        assert items['id'] == user.id
        assert items['username'] == user.username
        assert items['email'] == user.email
    
    def test_patch_users(self, client):
        user = User(
            username='Jack Black',
            email='jackblack@gmail.com',
            password_hash='jackblack123',
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
        
        data_updated = response.json
        items=data_updated['data']
        
        updated_user = db.session.get(User, user.id)
        
        assert items['email'] == user.email
        assert updated_user.username == new_username
    
    def test_get_records(self, client):
        
        user = User(
            username='testuser',
            email='test@example.com',
            password_hash='test123',
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
        
        data_updated = response.json
        items=data_updated['data']
        total=data_updated['total']
        
        records = Record.query.all()
        
        assert total
        assert [r['id'] for r in items] == [r.id for r in records]
        assert [r['title'] for r in items] == [r.title for r in records]
        assert [r['type'] for r in items] == [r.type for r in records]
        assert [r['description'] for r in items] == [r.description for r in records]
        assert [r['status'] for r in items] == [r.status for r in records]
        
    
    def test_get_records_by_id(self, client):
        user = User(
            username='testuser',
            email='test@example.com',
            password_hash='test123',
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
        
        data_updated = response.json
        items=data_updated['data']
        
        assert items['id'] == record.id
        assert items['status'] == record.status
        assert items['description'] == record.description
        assert items['type'] == record.type
        assert items['title'] == record.title
    
    def test_patch_records(self, client):
        user = User(
            username='testuser',
            email='test@example.com',
            password_hash='test123',
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
        data_updated = response.json
        
        items=data_updated['data']
        
        updated_record = db.session.get(Record, record.id)
        
        assert items['id'] == updated_record.id
        assert items['status'] == updated_record.status
        assert items['description'] == updated_record.description
        assert items['type'] == updated_record.type
        assert 'updated' in updated_record.title