import pytest
from server.models.video.video import Video 
from server.models.record.record import Record
from server.config import db 


class TestVideo: 

    def test_video_instance(self):
        video = Video()
        assert isinstance(video, Video)


    def test_video_creation(self):
        video = Video(
            video_url="video.mp4",
            record_id=1
        )

        assert video.video_url == "video.mp4"
        assert video.record_id == 1


    def test_video_save(self, app):
        record = Record(
            title="Test",
            description="Test description",
            type="red flag"
        )
        db.session.add(record)
        db.session.commit()

        video = Video(
            video_url="video.mp4",
            record_id=record.id
        )
        db.session.add(video)  

        assert video.id is not None   


    def test_video_requires_url(self):
        with pytest.raises(ValueError):
            Video(
                video_url=None,
                record_id=1
            )


    def test_video_belongs_to_record(self, app):
        record = Record(
            title="Test",
            description="Test description",
            type="red flag"
        )
        db.session.add(record)
        db.session.commit()

        video = Video(
            video_url="video.mp4",   
        )
        db.session.add(video)
        db.session.commit()

        assert video.record == record


    def test_create_video(self, client):
        client.post('/records', json={
            "title": "Test",
            "description": "Test description",
            "type": "red flag"
        })

        response = client.post('/videos', json={
            "video_url": "video.mp4",
            "record_id": 1
        })

        assert response.status_code == 201


    def test_get_videos(self, client):
        response = client.get('/videos')
        assert response.status_code == 200


    def test_delete_video(self, client): 
        client.post('/records', json={
            "title": "Test",
            "description": "Test description",
            "type": "red flag"
        })

        client.post('/videos', json={
            "video_url": "video.mp4",
            "record_id": 1
        })

        response = client.delete('/videos/1')

        assert response.status_code == 200