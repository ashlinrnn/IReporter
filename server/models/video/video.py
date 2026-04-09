from sqlalchemy_serializer import SerializerMixin
from sqlalchemy.orm import validates
from ...config import db 


class Video(db.Model, SerializerMixin):
    __tablename__ = 'videos' 
    
    #serialize_rules = ("-record.videos")
    id = db.Column(db.Integer, primary_key=True)
    record_id = db.Column(db.Integer, db.ForeignKey("records.id"), nullable= False)
    video_url = db.Column(db.Text, nullable = False)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    
    #record = db.relationship('Record', backref=db.backref('videos', lazy=True)) 

    @validates('video_url')
    def validate_video_url(self, key, value):
        if not value:
            raise ValueError('Video URL must be provided')
        return value