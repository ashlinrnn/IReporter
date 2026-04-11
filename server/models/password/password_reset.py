from ...config import db
from datetime import datetime, timedelta
import random

class PasswordReset(db.Model):
    __tablename__ = 'password_resets'

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), nullable=False, index=True)
    code = db.Column(db.String(6), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    expires_at = db.Column(db.DateTime, default=lambda: datetime.utcnow() + timedelta(minutes=10))

    @classmethod
    def generate_code(cls):
        return f"{random.randint(100000, 999999)}"

    @classmethod
    def create_reset_code(cls, email):
        # delete old codes for this email
        cls.query.filter_by(email=email).delete()
        code = cls.generate_code()
        reset = cls(email=email, code=code)
        db.session.add(reset)
        db.session.commit()
        return code