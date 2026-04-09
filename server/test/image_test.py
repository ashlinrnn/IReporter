from server.models.image.image import Image
from server.config import db
from sqlalchemy_serializer import SerializerMixin

class TestImage:
    def test_instance(self):
        img = Image()
        assert isinstance(img, Image)

    def test_attributes(self):
        img = Image(image_url="img.png", record_id=1)
        assert img.id is None
        assert img.image_url == "img.png"
        assert img.record_id == 1

    def test_inheritance(self):
        img = Image()
        assert isinstance(img, db.Model)
        assert isinstance(img, SerializerMixin)

    def test_to_dict(self):
        img = Image(image_url="img.png", record_id=1)
        assert isinstance(img.to_dict(), dict)