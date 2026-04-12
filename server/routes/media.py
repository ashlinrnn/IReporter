from flask import request
from flask_restful import Resource
from server.services.cloudinary import upload_image, upload_video
from server.models.image.image import Image
from server.models.video.video import Video
from server.config import db


class UploadImage(Resource):
    def post(self):
        file = request.files.get('image')
        record_id = request.form.get('record_id')

        if not file or not record_id:
            return {"message": "Missing file or record_id"}, 400

        url = upload_image(file)

        image = Image(image_url=url, record_id=record_id)
        db.session.add(image)
        db.session.commit()

        return {"data": {"id": image.id, "image_url": image.image_url}}, 201


class UploadVideo(Resource):
    def post(self):
        file = request.files.get('video')
        record_id = request.form.get('record_id')

        if not file or not record_id:
            return {"message": "Missing file or record_id"}, 400

        url = upload_video(file)

        video = Video(video_url=url, record_id=record_id)
        db.session.add(video)
        db.session.commit()

        return {"data": {"id": video.id, "video_url": video.video_url}}, 201