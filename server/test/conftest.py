import pytest
from server.app import create_app
from server.config import db as _db
from server.models.user.user import User

@pytest.fixture(scope='session')
def app():
    app = create_app()
    app.config['TESTING'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    with app.app_context():
        _db.create_all()
        yield app
        _db.drop_all()

@pytest.fixture(scope='function')
def db(app):
    yield _db
    _db.session.rollback()

@pytest.fixture(scope='function')
def client(app):
    return app.test_client()

@pytest.fixture(scope='function')
def test_user(app, db):
    user = User(
        username="testuser",
        email="testuser@example.com",
        password="password123"
    )
    db.session.add(user)
    db.session.commit()
    return user