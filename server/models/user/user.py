from sqlalchemy_serializer import SerializerMixin
from sqlalchemy.orm import validates
from ...config import db

class User(db.Model, SerializerMixin):
    
    __tablename__='users'
    
    serialize_rules=('-records.user',)
    
    id=db.Column(db.Integer, primary_key=True)
    username=db.Column(db.String, unique=True, nullable=False)
    email=db.Column(db.String, unique=True, nullable=False)
    password_hash=db.Column(db.String, nullable=False)
    is_admin=db.Column(db.Boolean, default=False)
    created_at=db.Column(db.DateTime, server_default=db.func.now())
    updated_at=db.Column(db.DateTime, server_default=db.func.now())
    
    records=db.relationship('Record', backref='user', cascade='all, delete-orphan')
    
    @validates('username')
    def validate_username(self,key,username):
        if not username:
            raise ValueError('Username needs to be present')
        return username
    
    @validates('email')
    def validate_email(self,key,email):
        if email and '@' in email:
            return email
        raise ValueError('Email needs to be present and in the correct format')
    
    
    def __repr__(self):
        return f'<User id:{self.id} name:{self.username} email:{self.email} >'
    
    