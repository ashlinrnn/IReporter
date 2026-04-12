from flask import request
from server.routes.create_blueprint import api_v1
from server.models.record.record import Record
from server.config import db


# ------------------ GET SINGLE RECORD (admin/user) ------------------
@api_v1.route('/records/me/<int:id>', methods=['GET'])
def get_record(id):
    record = Record.query.get(id)

    if not record:
        return {"message": "Record not found"}, 404

    return {
        "data": {
            "id": record.id,
            "title": record.title,
            "description": record.description,
            "status": record.status,
            "user_id": record.user_id
        }
    }, 200


# ------------------ CREATE RECORD ------------------
@api_v1.route('/records/create', methods=['POST'])
def create_record():
    data = request.json

    if not data:
        return {"message": "No input data provided"}, 400

    record = Record(
        title=data.get("title"),
        description=data.get("description"),
        type=data.get("type"),
        status=data.get("status", "pending"),
        user_id=data.get("user_id")
    )

    db.session.add(record)
    db.session.commit()

    return {
        "data": {
            "id": record.id,
            "title": record.title
        }
    }, 201


# ------------------ ADMIN UPDATE STATUS ------------------
@api_v1.route('/admin/records/<int:id>/status', methods=['PATCH'])
def update_status(id):
    record = Record.query.get(id)

    if not record:
        return {"message": "Record not found"}, 404

    data = request.json
    record.status = data.get("status", record.status)

    db.session.commit()

    return {
        "data": {
            "id": record.id,
            "status": record.status
        }
    }, 200