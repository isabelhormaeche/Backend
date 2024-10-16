from typing import List, Optional
from fastapi import APIRouter, Depends, status, HTTPException, Form, File, UploadFile
from sqlalchemy.orm import Session
import logging

from .. import schemas, database, oauth2
from ..crud import blog


router = APIRouter(
    prefix="/api/blogs",
    tags=['Blogs']
)

get_db = database.get_db


# *************** Route behind authentication**********************

# CREATE POST (with image)
# TODO añadir validaciones ***********************AÑADIR  user id y date?????????????

## Allowed image types and max size:
ALLOWED_IMAGE_TYPES = ["image/jpeg", "image/png"]
MAX_IMAGE_SIZE = 2 * 1024 * 1024  # 2 MB

## logger configuration:
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.ShowBlog)
async def create_blog(
    title: str = Form(...),
    desc: str = Form(...),
    cat: str = Form(...),
    # file: UploadFile = File(...),
    image: UploadFile = File(...), # changed like frontend
    db: Session = Depends(get_db),
    current_user: schemas.User = Depends(oauth2.get_current_user)
):
    
     # Validate and process data using schema BlogBase ****
    blog_data = schemas.BlogBase(title=title, desc=desc, cat=cat)


    logger.info(f"Received file: {image.filename}")
    if image.content_type not in ALLOWED_IMAGE_TYPES:
        logger.error("Invalid image type")
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid image type. Only JPEG and PNG are allowed.")
    
    contents = await image.read()
    if len(contents) > MAX_IMAGE_SIZE:
        logger.error("Image size exceeds the maximum limit")
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Image size exceeds the maximum limit of 2 MB.")
    
    file_location = f"uploadImage/{image.filename}"
    try:
        with open(file_location, "wb") as buffer:
            buffer.write(contents)
        logger.info(f"File saved at {file_location}")
    except Exception as e:
        logger.error(f"Error saving file: {e}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal server error")
    
    try:
        user_id=1  # Added user id manually for testing
        # return blog.create_blog(db, title, desc, cat, file_location, user_id)   ****

        return blog.create_blog(db, blog_data.title, blog_data.desc, blog_data.cat, file_location, user_id)
    
    except Exception as e:
        logger.error(f"Error creating blog: {e}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal server error")


##******************************end of create blog*****************************************


# GET ALL location blogs BY CATEGORY(if any), if none, get all:

@router.get("/", response_model=List[schemas.ShowBlog])
def get_blogs(cat: Optional[str] = None, db: Session = Depends(get_db)):
    return blog.get_blogs_cat(cat, db)



# GET ONE LOCATION BLOG

@router.get("/{id}", status_code=200, response_model=schemas.ShowBlog)
def get_one(id:int, db:Session= Depends(database.get_db)):
    return blog.get_one_blog(id, db)



# *************** Route behind authentication**********************

# DELETE ONE LOCATON BLOG

@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete(id, db: Session = Depends(get_db), current_user: schemas.User = Depends(oauth2.get_current_user)):
    return blog.delete_blog(id, db)



# *************** Route behind authentication**********************

# UPDATE ONE LOCATION BLOG

# TODO añadir validaciones y raise excepciones

# No need ANY DATE pero sí USER ID!!!!!!!!!!!!!!!!!!!!!!!!!!
# condición de id y udi para editar
@router.put("/update_blog/{blog_id}", status_code=status.HTTP_200_OK, response_model=schemas.ShowBlog)
async def update_blog(blog_id: int, title: Optional[str] = Form(None), desc: Optional[str] = Form(None), cat: Optional[str] = Form(None), image: Optional[UploadFile] = None, db: Session = Depends(get_db), current_user: schemas.User = Depends(oauth2.get_current_user)):
    
    # Validate and process data using schema BlogUpdate ****
    blog_data = schemas.BlogUpdate(title=title, desc=desc, cat=cat)
    
    file_location = None  # new thing
    if image is not None:
        contents = await image.read()
        file_location = f"uploadImage/{image.filename}"
        with open(file_location, "wb") as buffer:
            buffer.write(contents)
    # return blog.update_blog(blog_id, db, title, desc, cat, file_location)
    return blog.update_blog(blog_id, db, blog_data.title, blog_data.desc, blog_data.cat, file_location)
