from flask import request,g, jsonify, make_response
from flask_restful import Resource
from server.models.image.image import Image
from server.config import db

class ImageResource(Resource):

    def post(self):
        data = request.get_json()

        image = Image(
            image_url=data['image_url'],
            record_id=data['record_id']
        )

        db.session.add(image)  
        db.session.commit()

        return make_response(image.to_dict(), 201)


    def get(self):
        images = [image.to_dict() for image in Image.query.all()]
        return make_response(images, 200)


class ImageByID(Resource):

    def get(self, id):
        image = Image.query.get(id)

        if not image:   
            return make_response({"error": "Image not found"}, 404)

        return make_response(image.to_dict(), 200)


    def delete(self, id):
        image = Image.query.get(id)

        if not image:
            return make_response({"error": "Image not found"}, 404)  
        db.session.delete(image)
        db.session.commit()

        return make_response("", 204)


    def patch(self, id):
        image = Image.query.get(id)

        if not image:
            return {"error": "Image not found"}, 404

        data = request.get_json()

        if 'image_url' in data:
            image.image_url = data['image_url']

        db.session.commit()

        return image.to_dict(), 200