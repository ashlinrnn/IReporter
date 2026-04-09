import pytest
from unittest.mock import patch, MagicMock
from server.app import create_app
from server.config import db
from server.models import User, Record
from server.utils.auth import create_token

@pytest.fixture(scope='module')
def app():
    """Create a Flask app instance for testing"""
    test_config={
        'TESTING':True,
        'SQLALCHEMY_DATABASE_URI':'sqlite:///:memory:',
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

def create_test_user_and_record():
    """Helper to create a regular user, an admin user, and a record."""
    # Regular user (record owner)
    user = User(
        username='owner',
        email='owner@example.com',
        password='password123',
        is_admin=False
    )
    db.session.add(user)
    db.session.commit()

    # Admin user
    admin = User(
        username='admin',
        email='admin@example.com',
        password='adminpass',
        is_admin=True
    )
    db.session.add(admin)
    db.session.commit()

    # Record owned by regular user
    record = Record(
        user_id=user.id,
        type='red flag',
        title='Test Corruption',
        description='Test description',
        status='pending'
    )
    db.session.add(record)
    db.session.commit()

    admin_token = create_token(admin.id)
    user_token = create_token(user.id)
    return user, admin, record, admin_token, user_token

@patch('server.models.record.routes.record_routes.send_status_update_email')
def test_email_sent_when_admin_changes_status(mock_send_email, client):
    """Test that email notification is triggered when admin changes record status."""
    
    user, admin, record, admin_token, user_token = create_test_user_and_record()
    headers = {'Authorization': f'Bearer {admin_token}'}
    
    # Mock the email function to return True (success)
    mock_send_email.return_value = True
    
    # Admin changes status 
    response = client.patch(
        f'/api/v1/admin/records/{record.id}/status',
        headers=headers,
        json={'status': 'under investigation'}
    )
    
    assert response.status_code == 200
    
    # Verify email function was called once with correct arguments
    mock_send_email.assert_called_once_with(
        recipient_email=user.email,
        recipient_name=user.username,
        record_title=record.title,
        new_status='under investigation'
    )

@patch('server.models.record.routes.record_routes.send_status_update_email')
def test_email_not_sent_for_non_status_update(mock_send_email, client):
    """Test that email is NOT sent when a non-admin updates non-status fields."""
    user, admin, record, admin_token, user_token = create_test_user_and_record()
    headers = {'Authorization': f'Bearer {user_token}'}
    
    response = client.patch(
        f'/api/v1/records/me/{record.id}',
        headers=headers,
        json={'title': 'Updated Title'}
    )
    
    assert response.status_code == 200
    # Email should NOT be called because status didn't change
    mock_send_email.assert_not_called()

@patch('server.models.record.routes.record_routes.send_status_update_email')
def test_email_failure_does_not_block_status_update(mock_send_email, client):
    """Test that even if email fails, the status update still succeeds."""
    user, admin, record, admin_token, user_token = create_test_user_and_record()
    headers = {'Authorization': f'Bearer {admin_token}'}
    
    # Simulate email failure
    mock_send_email.return_value = False
    
    response = client.patch(
        f'/api/v1/admin/records/{record.id}/status',
        headers=headers,
        json={'status': 'resolved'}
    )
    
    # Status update should still succeed
    assert response.status_code == 200
    
    # Verify email was attempted
    mock_send_email.assert_called_once()
    
    # Check that status actually changed in database
    updated_record = db.session.get(Record, record.id)
    assert updated_record.status == 'resolved'