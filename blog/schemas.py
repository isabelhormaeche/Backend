from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional, List

class BlogBase(BaseModel):
    title: str = Field(..., min_length=1, max_length=100)
    desc: str = Field(..., min_length=1, max_length=1000)
    cat: str = Field(..., min_length=1, max_length=50)
    image: Optional[str] = None  

class Blog(BlogBase):
     class Config:
         from_attributes = True

class BlogUpdate(BaseModel):
    title: Optional[str] = Field(None, min_length=1, max_length=100)
    desc: Optional[str] = Field(None, min_length=1, max_length=1000)
    cat: Optional[str] = Field(None, min_length=1, max_length=50)
    image: Optional[str] = None
    

#******************* SCHEMAS FOR THE USER******************

class User(BaseModel):
     name: str
     email: str
     password: str

     class Config:
         from_attributes = True

class ShowUser(BaseModel):
    id: int
    name: str
    email: str
    # blogs : List[BlogBase] =[]
    blogs : List[BlogBase] =[]
# does not show the password
    class Config:
        from_attributes = True

class ShowBlog(BlogBase):
    id: int
    date: datetime  
    cat: Optional[str] = None 
    user_id:int
    owner: ShowUser
    
    class Config:
        from_attributes = True


# Authentication schemas

class Login(BaseModel):
    username: str
    password:str
    class Config:
        from_attributes = True


class Token(BaseModel):
     access_token: str
     token_type: str


class TokenData(BaseModel):
     email: Optional[str] = None

     

     



