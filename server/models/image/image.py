from sqlalchemy_serializer import SerializerMixin
from sqlalchemy.orm import validates
from ...config import db 

class Image(db.Model, SerializerMixin):
    
    __tablenamename__ = "images" 

    serialize_rules = ('-record.images')

    id = db.Column(db.Integer, primary_key=True)
    record_id = db.Column(db.Integer, db.ForeignKey("reports.id"), nullable= False)
    image_url = db.Column(db.Text, nullable = False)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    
    record = db.relationship('Record', backref=db.backref('images', lazy=True))