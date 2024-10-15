from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from .database import Base
import datetime
from sqlalchemy.orm import relationship


class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=False)
    password = Column(String, nullable=False)

    blogs = relationship('Blog', back_populates="owner")



class Blog(Base):
    __tablename__ = 'blogs'

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    image = Column(String, nullable=True)
    desc = Column(String, nullable=False)
    cat = Column(String, nullable=False)
    date = Column(DateTime, default=datetime.datetime.utcnow)
    user_id = Column(Integer, ForeignKey("users.id"))

    owner = relationship("User", back_populates="blogs")







 # https://fastapi.tiangolo.com/tutorial/sql-databases/