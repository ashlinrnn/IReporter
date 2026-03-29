from ...config import db
from sqlalchemy_serializer import SerializerMixin
from sqlalchemy.orm import validates

class Record(db.Model, SerializerMixin):
    __tablename__='reports'
    
    serialize_rules=('-images.record', '-videos.record',)
    
    id=db.Column(db.Integer, primary_key=True)
    user_id=db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    type=db.Column(db.Enum('red flag', 'intervention', name='record_tyoe'), nullable=False)
    title=db.Column(db.String, nullable=False)
    description=db.Column(db.Text, nullable=False)
    status=db.Column(db.Enum('pending', 'under investigation', 'rejected', 'resolved', name='record_status'), default='pending')
    latitude=db.Column(db.Float)
    longitude=db.Column(db.Float)
    created_at=db.Column(db.DateTime, server_default=db.func.now())
    updated_at=db.Column(db.DateTime, server_default=db.func.now(), onupdate=db.func.now())
    
    images=db.relationship('Image', backref='record', cascade='all, delete-orphan')
    videos=db.relationship('Video', backref='record', cascade='all, delete-orphan')