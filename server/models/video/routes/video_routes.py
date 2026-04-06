from flask import request,g, jsonify, make_response
from flask_restful import Resource
from server.models.video.video import Video
from server.config import db


class VideoResource(Resource):

    def post(self):
        data = request.get_json()

        video = Video(
            video_url=data['video_url'],
            record_id=data['record_id']
        )

        db.session.add(video)  
        db.session.commit()

        return make_response(video.to_dict(), 201)


    def get(self):
        videos = [video.to_dict() for video in Video.query.all()]
        return make_response(videos, 200)


class VideoByID(Resource):

    def get(self, id):
        video = Video.query.get(id)

        if not video:   
            return make_response({"error": "Video not found"}, 404)

        return make_response(video.to_dict(), 200)


    def delete(self, id):
        video = Video.query.get(id)

        if not video:
            return make_response({"error": "video not found"}, 404)  
        db.session.delete(video)
        db.session.commit()

        return make_response("", 204)


    def patch(self, id):
        video = Video.query.get(id)

        if not video:
            return {"error": "Video not found"}, 404

        data = request.get_json()

        if 'video_url' in data:
            video.video_url = data['video_url']

        db.session.commit()

        return video.to_dict(), 200