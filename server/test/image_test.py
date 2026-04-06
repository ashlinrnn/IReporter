from server.models.image.image import Image
from server.config import db
from sqlalchemy_serializer import SerializerMixin

class TestImage:

    def test_instance(self):
        image = Image()
        assert isinstance(image, Image)

    def test_has_attributes(self):
        image = Image(
            image_url="test.jpg",
            record_id=1
        )
        assert image.id is None
        assert image.image_url == "test.jpg"
        assert image.record_id == 1

    def test_inheritance(self):
        image = Image()
        assert isinstance(image, SerializerMixin)
        assert isinstance(image, db.Model)

    def test_to_dict(self):
        image = Image(
            image_url="test.jpg",
            record_id=1
        )
        data = image.to_dict()
        assert isinstance(data, dict)
        assert data["image_url"] == "test.jpg"
        assert data["record_id"] == 1