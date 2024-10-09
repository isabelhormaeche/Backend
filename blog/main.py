import logging
from fastapi import FastAPI, Depends, status, Response, HTTPException, UploadFile, File, Form
from sqlalchemy.orm import Session
from . import schemas, models
from .database import engine, SessionLocal
from typing import List, Optional
import os
from .database import get_db
from fastapi.middleware.cors import CORSMiddleware


app = FastAPI()

# TODO Change origin when send to production *************************
origin = [
    'http://localhost:3000'
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origin,
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*']
    )

models.Base.metadata.create_all(engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

    
# UPLOAD image with FastAPI

# https://fastapi.tiangolo.com/tutorial/request-files/#file-parameters-with-uploadfile
# https://youtu.be/m6Ma6B6VlFs?feature=shared
# https://galaxyofai.com/how-to-send-images-to-python-fastapi-using-postman/

ALLOWED_IMAGE_TYPES = ["image/jpeg", "image/png"]
MAX_IMAGE_SIZE = 2 * 1024 * 1024  # 2 MB

# logger configuration:
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@app.post("api/upload_image", status_code=status.HTTP_201_CREATED)
async def upload_image(file: UploadFile = File(...)):
    logger.info(f"Received file: {file.filename}")
    if file.content_type not in ALLOWED_IMAGE_TYPES:
        logger.error("Invalid image type")
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid image type. Only JPEG and PNG are allowed.")
    
    contents = await file.read()
    if len(contents) > MAX_IMAGE_SIZE:
        logger.error("Image size exceeds the maximum limit")
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Image size exceeds the maximum limit of 2 MB.")
    
    file_location = f"uploadImage/{file.filename}"
    try:
        with open(file_location, "wb") as buffer:
            buffer.write(contents)
        logger.info(f"File saved at {file_location}")
    except Exception as e:
        logger.error(f"Error saving file: {e}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal server error")
    
    return {"file_location": file_location}

# Just in case --> create folder for the images
if not os.path.exists('uploadImage'):
    os.makedirs('uploadImage')



# Create location blogs

# TODO añadir validaciones y raise excepciones  

@app.post("api/create_blog", status_code=status.HTTP_201_CREATED, response_model=schemas.ShowBlog)
async def create_blog(blog: schemas.BlogCreate, db: Session = Depends(get_db)):
    try:
        new_blog = models.Blog(title=blog.title, desc=blog.desc, cat=blog.cat, image=blog.image)
        db.add(new_blog)
        db.commit()
        db.refresh(new_blog)
        
        return new_blog
    except Exception as e:
        logger.error(f"Error creating blog: {e}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal server error")


   

# Get all location blogs

@app.get("api/blog", response_model=List[schemas.ShowBlog])
def get_all(db: Session = Depends(get_db)):
    blogs = db.query(models.Blog).all()
    return blogs



# Get location blogs by category

@app.get("api/blog/category/{cat}", response_model=list[schemas.ShowBlog])
def get_by_category(cat: str = None, db: Session = Depends(get_db)):
    blogs =db.query(models.Blog).filter(models.Blog.cat == cat).all()
    if not blogs:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"No blogs found in category{cat}")
    return blogs


### TODO asegurarme que manda blog id***********************************
# Get one location blog

@app.get("api/blog/{id}", status_code=200, response_model=schemas.ShowBlog)
def get_one(id, response: Response, db:Session= Depends(get_db)):
    blog = db.query(models.Blog).filter(models.Blog.id == id).first()
    if not blog:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Blog with id {id} is not available")
        # response.status_code = status.HTTP_404_NOT_FOUND
        # return{"detail": f"Blog with id {id} is not available"}
    return blog


# Delete one location blog

@app.delete("api/blog/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete(id, db: Session = Depends(get_db)):
    blog = db.query(models.Blog).filter(models.Blog.id ==id)
    if not blog.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Blog with id {id} is not available")
    blog.delete(synchronize_session=False)
    db.commit()
    return "The blog was deleted successfully"



# Update one location blog

# TODO añadir validaciones y raise excepciones


@app.put("api/update_blog/{blog_id}", status_code=status.HTTP_200_OK, response_model=schemas.ShowBlog)
async def update_blog(blog_id: int, title: Optional[str] = Form(None), desc: Optional[str] = Form(None), cat: Optional[str] = Form(None), image: Optional[UploadFile] = None, db: Session = Depends(get_db)):
    blog_to_update = db.query(models.Blog).filter(models.Blog.id == blog_id).first()
    
    if not blog_to_update:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Blog not found")
    
    if title is not None:
        blog_to_update.title = title
    if desc is not None:
        blog_to_update.desc = desc
    if cat is not None:
        blog_to_update.cat = cat
    if image is not None:
        contents = await image.read()
        file_location = f"uploadImage/{image.filename}"
        with open(file_location, "wb") as buffer:
            buffer.write(contents)
        blog_to_update.image = file_location
    
    db.commit()
    db.refresh(blog_to_update)
    
    return blog_to_update



# Delete all the blogs (TODO: borrar luego porque es para desarrollo solo)

@app.delete("api/blogs", status_code=status.HTTP_204_NO_CONTENT)
def delete_all_blogs(db: Session = Depends(get_db)):
    db.query(models.Blog).delete()
    db.commit()
    return {"detail": "All blogs deleted successfully"}


