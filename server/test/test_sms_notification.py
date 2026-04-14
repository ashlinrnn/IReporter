import pytest
from unittest.mock import patch
from server.app import create_app
from server.config import db
from server.models import User, Record
from server.utils.auth import create_token

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

_counter = 0 #create unique emails

def create_user_with_phone(phone_number=None, is_admin=False):
    global _counter
    _counter += 1
    username = f'testuser_{_counter}'
    email = f'test_{_counter}@example.com'
    user = User(
        username=username,
        email=email,
        password='password123',
        is_admin=is_admin,
        phone_number=phone_number
    )
    db.session.add(user)
    db.session.commit()
    return user

def create_record(user_id, status='pending'):
    record = Record(
        user_id=user_id,
        type='red flag',
        title='Test Corruption',
        description='Test description',
        status=status
    )
    db.session.add(record)
    db.session.commit()
    return record


@patch('server.models.record.routes.record_routes.sms_service.send_sms')
def test_sms_sent_when_user_has_phone_number(mock_send_sms, client):
    user = create_user_with_phone(phone_number='+254712345678')
    record = create_record(user.id)
    admin = create_user_with_phone(is_admin=True)
    admin_token = create_token(admin.id)
    headers = {'Authorization': f'Bearer {admin_token}'}

    response = client.patch(
        f'/api/v1/admin/records/{record.id}/status',
        headers=headers,
        json={'status': 'under investigation'}
    )
    assert response.status_code == 200

    mock_send_sms.assert_called_once()
    args, kwargs = mock_send_sms.call_args
    assert args[0] == user.phone_number
    assert f"Status of report '{record.title}' changed to 'under investigation'" in args[1]


@patch('server.models.record.routes.record_routes.sms_service.send_sms')
def test_sms_not_sent_when_user_no_phone_number(mock_send_sms, client):
    user = create_user_with_phone(phone_number=None)
    record = create_record(user.id)
    admin = create_user_with_phone(is_admin=True)
    admin_token = create_token(admin.id)
    headers = {'Authorization': f'Bearer {admin_token}'}

    response = client.patch(
        f'/api/v1/admin/records/{record.id}/status',
        headers=headers,
        json={'status': 'under investigation'}
    )
    assert response.status_code == 200
    mock_send_sms.assert_not_called()

@patch('server.models.record.routes.record_routes.sms_service.send_sms')
def test_sms_failure_does_not_block_status_update(mock_send_sms, client):
    user = create_user_with_phone(phone_number='+254712345678')
    record = create_record(user.id)
    admin = create_user_with_phone(is_admin=True)
    admin_token = create_token(admin.id)
    headers = {'Authorization': f'Bearer {admin_token}'}

    mock_send_sms.return_value = False

    response = client.patch(
        f'/api/v1/admin/records/{record.id}/status',
        headers=headers,
        json={'status': 'resolved'}
    )
    assert response.status_code == 200
    mock_send_sms.assert_called_once()

    updated_record = db.session.get(Record, record.id)
    assert updated_record.status == 'resolved'

@patch('server.models.record.routes.record_routes.sms_service.send_sms')
def test_sms_correct_message_format(mock_send_sms, client):
    user = create_user_with_phone(phone_number='+254712345678')
    record = create_record(user.id)
    admin = create_user_with_phone(is_admin=True)
    admin_token = create_token(admin.id)
    headers = {'Authorization': f'Bearer {admin_token}'}

    new_status = 'rejected'
    response = client.patch(
        f'/api/v1/admin/records/{record.id}/status',
        headers=headers,
        json={'status': new_status}
    )
    assert response.status_code == 200

    mock_send_sms.assert_called_once()
    args, kwargs = mock_send_sms.call_args
    assert args[0] == user.phone_number
    assert f"Status of report '{record.title}' changed to '{new_status}'" in args[1]