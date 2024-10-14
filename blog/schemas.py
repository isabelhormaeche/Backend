from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional

class BlogBase(BaseModel):
    title: str = Field(..., min_length=1, max_length=100)
    desc: str = Field(..., min_length=1, max_length=1000)
    cat: str = Field(..., min_length=1, max_length=50)
    image: Optional[str] = None  

class BlogCreate(BlogBase):
    pass

class ShowBlog(BlogBase):
    id: int
    date: datetime  
    cat: Optional[str] = None # the category is optional
    
    class Config:
        orm_mode = True

#******************* SCHEMAS FOR THE USER******************

# class User(BaseModel):
#     name:str
#     email:str
#     password:str



