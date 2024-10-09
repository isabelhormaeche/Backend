from sqlalchemy import Column, Integer, String, DateTime
#from sqlalchemy.sql import func
from .database import Base
import datetime

class Blog(Base):
    __tablename__ = 'blogs'

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    image = Column(String, nullable=True)
    desc = Column(String, nullable=False)
    cat = Column(String, nullable=False)
    #date = Column(DateTime(timezone=True), server_default=func.now())  
    date = Column(DateTime, default=datetime.datetime.utcnow)