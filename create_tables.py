from sqlalchemy import create_engine
from blog.models import Base

engine = create_engine('sqlite:///./blog.db')
Base.metadata.create_all(engine)
