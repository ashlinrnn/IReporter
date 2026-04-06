from server.models.user.user import User
from server.app import create_app
from sqlalchemy_serializer import SerializerMixin
from server.config import db

class TestUser:
    
    def test_instance(self):
        user=User()
        assert isinstance(user,User)
    
    def test_has_attri(self):
        user = User(
            username='Jack Black',
            email='jackblack@gmail.com',
            password='jackblack123',
        )
        assert user.id is None
        assert user.username == 'Jack Black'
        assert user.email == 'jackblack@gmail.com'
        assert user.password_hash != 'jackblack123'  
        
    def test_inheritance(self):
        user=User()
        assert isinstance(user, SerializerMixin)
        assert isinstance(user, db.Model)
    
    def test_to_dict(self):
        user = User(
            username='Jack Black',
            email='jackblack@gmail.com',
            password='jackblack123',     
        )
        assert isinstance(user.to_dict(), dict)
        
    def test_password_hash(self):
        password='1234red'
        user=User(
            username='Jack Black',
            email='jackblack@gmail.com',
            password=password,
        )
        
        assert user.password_hash!=password
        
        assert user.password_hash.startswith('$2b$')
        
        assert user.authenticate(password) is True
        
        assert user.authenticate('wrong') is False
    