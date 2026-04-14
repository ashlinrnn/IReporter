from sqlalchemy_serializer import SerializerMixin
from sqlalchemy.orm import validates
from ...config import db, bcrypt
from sqlalchemy.ext.hybrid import hybrid_property

class User(db.Model, SerializerMixin):
    
    __tablename__='users'
    
    serialize_rules=('-records.user','-password_hash','-created_at', '-updated_at')
    
    id=db.Column(db.Integer, primary_key=True)
    username=db.Column(db.String, unique=True, nullable=False)
    email=db.Column(db.String, unique=True, nullable=False)
    phone_number=db.Column(db.String(20), nullable=True)
    password_hash=db.Column(db.String, nullable=False)
    phone_number=db.Column(db.String(20), nullable=True)
    profile_pic_url=db.Column(db.String, nullable=True)
    is_admin=db.Column(db.Boolean, default=False)
    created_at=db.Column(db.DateTime, server_default=db.func.now())
    updated_at=db.Column(db.DateTime, server_default=db.func.now())
    
    records=db.relationship('Record', backref='user', cascade='all, delete-orphan')
    
    def __init__(self,**kwargs):
        password=kwargs.pop('password',None)
        super().__init__(**kwargs)
        if password:
            self.password=password
    
    @hybrid_property
    def password(self):
        raise AttributeError('Can not access Attribute')
    
    @password.setter
    def password(self,password):
        
        self.password_hash=bcrypt.generate_password_hash(password.encode('utf-8')).decode('utf-8')
        
    def authenticate(self,password):
        return bcrypt.check_password_hash(self.password_hash, password.encode('utf-8'))
    
    
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