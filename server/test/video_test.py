from server.models.video.video import Video
from server.config import db
from sqlalchemy_serializer import SerializerMixin

class TestVideo:

    def test_instance(self):
        video = Video()
        assert isinstance(video, Video)

    def test_has_attributes(self):
        video = Video(
            video_url="test.mp4",
            record_id=1
        )
        assert video.id is None
        assert video.video_url == "test.mp4"
        assert video.record_id == 1

    def test_inheritance(self):
        video = Video()
        assert isinstance(video, SerializerMixin)
        assert isinstance(video, db.Model)

    def test_to_dict(self):
        video = Video(
            video_url="test.mp4",
            record_id=1
        )
        data = video.to_dict()
        assert isinstance(data, dict)
        assert data["video_url"] == "test.mp4"
        assert data["record_id"] == 1
