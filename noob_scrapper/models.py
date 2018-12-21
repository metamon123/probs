from sqlalchemy import Column, Integer, String
from database import Base

class User(Base):
    __tablename__ = 'Users'
    _id = Column(Integer, primary_key=True)
    id = Column(String(16))
    pw = Column(String)

    def __init__(self, id, pw):
        self.id = id[:16]
        self.pw = pw

    def __repr__(self):
        return "<User('%d', '%s', '%s'>" %(self._id, self.id, self.pw)
