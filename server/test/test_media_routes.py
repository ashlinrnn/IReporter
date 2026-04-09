import pytest
from server.app import create_app
from server.config import db
from server.models.record.record import Record
from ..test.test_user_specific_routes import create_user

# ------------------ Fixtures ------------------

@pytest.fixture(scope="module")
def app():
    app = create_app()
    app.config["TESTING"] = True
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///:memory:"
    return app

@pytest.fixture
def client(app):
    with app.app_context():
        db.create_all()
        yield app.test_client()
        db.session.remove()
        db.drop_all()

@pytest.fixture
def user(client):
    with client.application.app_context():
        u, _token = create_user()  # unpack tuple; only add model instance
        db.session.add(u)
        db.session.commit()
        yield u
        db.session.delete(u)
        db.session.commit()

@pytest.fixture
def record(user, client):
    with client.application.app_context():
        r = Record(
            title="Test Record",
            description="desc",
            type="red flag",
            status="pending",
            user_id=user.id
        )
        db.session.add(r)
        db.session.commit()
        yield r
        db.session.delete(r)
        db.session.commit()

# ------------------ Generic CRUD Helper ------------------

def generic_crud_test(client, endpoint, record_id, field_name, test_value, new_value):
    # CREATE
    res = client.post(endpoint, json={field_name: test_value, "record_id": record_id})
    assert res.status_code == 201
    obj_id = res.json["data"]["id"]
    assert res.json["data"][field_name] == test_value

    # GET ALL
    res = client.get(endpoint)
    assert res.status_code == 200
    items = res.json["data"]
    assert any(i["id"] == obj_id for i in items)

    # PATCH
    res = client.patch(f"{endpoint}/{obj_id}", json={field_name: new_value})
    assert res.status_code == 200
    assert res.json["data"][field_name] == new_value

    # DELETE
    res = client.delete(f"{endpoint}/{obj_id}")
    assert res.status_code == 204
    get_res = client.get(f"{endpoint}/{obj_id}")
    assert get_res.status_code == 404

# ------------------ Media Tests ------------------

class TestGenericMediaRoutes:
    def test_image_crud(self, client, record):
        generic_crud_test(
            client,
            endpoint="/api/v1/images",
            record_id=record.id,
            field_name="image_url",
            test_value="test.png",
            new_value="new.png",
        )

    def test_video_crud(self, client, record):
        generic_crud_test(
            client,
            endpoint="/api/v1/videos",
            record_id=record.id,
            field_name="video_url",
            test_value="test.mp4",
            new_value="new.mp4",
        )