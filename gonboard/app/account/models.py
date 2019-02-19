from sqlalchemy import Column, Integer, String
from werkzeug.security import generate_password_hash, check_password_hash
from app import Base


class User(Base):
    __tablename__ = 'Users'
    _id = Column(Integer, primary_key=True)
    uid = Column(String, unique=True)
    upw = Column(String)
    msg = Column(String)
    email = Column(String) # same people can have multiple acc

    def __init__(self, uid, upw, msg, email):
        self.uid = uid
        self.set_password(upw)
        self.msg = msg
        self.email = email

    def set_password(self, upw):
        self.upw = generate_password_hash(upw)
    
    def check_password(self, upw):
        return check_password_hash(self.upw, upw)

    def is_active(self):
        """True, as all users are active."""
        return True

    def get_id(self):
        """Return the email address to satisfy Flask-Login's requirements."""
        return self.uid

    def is_authenticated(self):
        """Return True if the user is authenticated."""
        return True

    def is_anonymous(self):
        """False, as anonymous users aren't supported."""
        return False

    def __repr__(self):
        return "<User('%d', '%s', '%s'>" % (self._id, self.uid, self.upw, self.msg, self.email)
