from sqlalchemy.orm import Session
from .. import models, schemas,  database

from fastapi import HTTPException,status
from typing import Optional

# get_db = database.get_db

# CREATE BLOG
def create_blog(db: Session, title: str, desc: str, cat: str, file_location: str, user_id: int):
    new_blog = models.Blog(title=title, desc=desc, cat=cat, image=file_location, user_id=user_id)
    db.add(new_blog)
    db.commit()
    db.refresh(new_blog)
    return new_blog


#  GET ALL location blogs BY CATEGORY(if any), if none, get all:
def get_all(db: Session):
    blogs = db.query(models.Blog).all()
    return blogs

def get_blogs_cat(cat: Optional[str], db: Session):
    if cat:
        blogs = db.query(models.Blog).filter(models.Blog.cat == cat).all()
        if not blogs:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"No blogs found in category {cat}")
    else:
        blogs = db.query(models.Blog).all()
    return blogs



# GET ONE LOCATION BLOG
def get_one_blog(id: int, db: Session):
    blog = db.query(models.Blog).filter(models.Blog.id == id).first()
    if not blog:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Blog with id {id} is not available")
    return blog


# DELETE ONE LOCATON BLOG
def delete_blog(id: int, db: Session):
    blog = db.query(models.Blog).filter(models.Blog.id == id)
    if not blog.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Blog with id {id} is not available")
    blog.delete(synchronize_session=False)
    db.commit()
    return "The blog was deleted successfully"


# UPDATE ONE LOCATION BLOG
def update_blog(blog_id: int, db: Session, title: Optional[str], desc: Optional[str], cat: Optional[str], file_location: Optional[str]):
    blog_to_update = db.query(models.Blog).filter(models.Blog.id == blog_id).first()
    if not blog_to_update:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Blog not found")
    
    if title is not None:
        blog_to_update.title = title
    if desc is not None:
        blog_to_update.desc = desc
    if cat is not None:
        blog_to_update.cat = cat
    if file_location is not None:
        blog_to_update.image = file_location
    
    db.commit()
    db.refresh(blog_to_update)
    return blog_to_update

