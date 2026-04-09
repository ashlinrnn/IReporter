from server.models.video.video import Video
from server.config import db
from sqlalchemy_serializer import SerializerMixin

class TestVideo:
    
    def test_instance(self):
        vid = Video()
        assert isinstance(vid, Video)
    
    def test_attributes(self):
        vid = Video(video_url="vid.mp4", record_id=1)
        assert vid.id is None
        assert vid.video_url == "vid.mp4"
        assert vid.record_id == 1
    
    def test_inheritance(self):
        vid = Video()
        assert isinstance(vid, db.Model)
        assert isinstance(vid, SerializerMixin)
    
    def test_to_dict(self):
        vid = Video(video_url="vid.mp4", record_id=1)
        assert isinstance(vid.to_dict(), dict)