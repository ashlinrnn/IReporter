from sqlalchemy_serializer import SerializerMixin
from sqlalchemy.orm import validates
from ...config import db 

class Image(db.Model, SerializerMixin):
    
    __tablenamename__ = "videos" 

    serialize_rules = ('-record.videos')

    id = db.Column(db.Integer, primary_key=True)
    record_id = db.Column(db.Integer, db.ForeignKey("reports.id"), nullable= False)
    image_url = db.Column(db.Text, nullable = False)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    
    record = db.relationship('Record', backref=db.backref('images', lazy=True)) 

    @validates('image_url')
    def validate_image_url(self, key, value):
        if not value:
            raise ValueError('Image URL must be provided')
        return value