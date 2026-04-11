from flask import request
from server.routes.create_blueprint import api_v1
from server.services.cloudinary import upload_image, upload_video
from server.models.image.image import Image
from server.models.video.video import Video
from server.config import db


# ------------------ IMAGE UPLOAD ------------------

@api_v1.route('/images/upload', methods=['POST'])
def upload_image_route():
    file = request.files.get('image')
    record_id = request.form.get('record_id')

    if not file or not record_id:
        return {"message": "Missing file or record_id"}, 400

    url = upload_image(file)

    if not url:
        return {"message": "Upload failed"}, 500

    image = Image(image_url=url, record_id=record_id)
    db.session.add(image)
    db.session.commit()

    return {
        "data": {
            "id": image.id,
            "image_url": image.image_url
        }
    }, 201


# ------------------ VIDEO UPLOAD ------------------

@api_v1.route('/videos/upload', methods=['POST'])
def upload_video_route():
    file = request.files.get('video')
    record_id = request.form.get('record_id')

    if not file or not record_id:
        return {"message": "Missing file or record_id"}, 400

    url = upload_video(file)

    if not url:
        return {"message": "Upload failed"}, 500

    video = Video(video_url=url, record_id=record_id)
    db.session.add(video)
    db.session.commit()

    return {
        "data": {
            "id": video.id,
            "video_url": video.video_url
        }
    }, 201