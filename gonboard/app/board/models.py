from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship, backref

from app import Base


class Post(Base):
    __tablename__ = 'Posts'
    _id = Column(Integer, primary_key=True)
    uploader = Column(String, unique=True)
    content = Column(String)
    # board_name which the post belongs to


class File(Base):
    __tablename__ = 'Files'
    _id = Column(Integer, primary_key=True)
    name = Column(String)
    post_id = Column(Integer, ForeignKey("Posts._id"))  # 이건 필요함
    post = relationship("Posts", backref=backref('files'))
    # board_id?
    # 전체?