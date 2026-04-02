from sqlalchemy_serializer import SerializerMixin
from sqlalchemy.orm import validates
from ...config import db 

class Image(db.model, SerializerMixin):
    
    __tablenamename__ = "images" 

    id = db.Column(db.Integer, primary_key=True)
    record_id = db.Column(db.Integer, db.ForeignKey("recors.id"), nullable= False)
    image_url = db.Column(db.Text, nullable = False)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    
    