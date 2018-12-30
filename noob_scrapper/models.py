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

class Scrap(Base):
    __tablename__ = "Scraps"
    _id = Column(Integer, primary_key=True)
    owner_id = Column(String(16))
    name = Column(String)
    title = Column(String)

    def __init__(self, owner_id, name, title):
        self.owner_id = owner_id
        self.name = name
        self.title = title

    def __repr__(self):
        return "<Scrap('%d', '%s', '%s', '%s'>" %(self._id, self.owner_id, self.name, self.title)
