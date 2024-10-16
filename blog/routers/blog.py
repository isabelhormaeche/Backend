from typing import List, Optional
from fastapi import APIRouter, Depends, status, HTTPException, Form, File, UploadFile
from .. import schemas, database
from sqlalchemy.orm import Session
import logging
from ..crud import blog

router = APIRouter(
    prefix="/api/blogs",
    tags=['Blogs']
)

get_db = database.get_db

# GET ALL location blogs BY CATEGORY(if any), if none, get all:

@router.get("/", response_model=List[schemas.ShowBlog])
def get_blogs(cat: Optional[str] = None, db: Session = Depends(get_db)):
    return blog.get_blogs_cat(cat, db)
#     try:
#         if cat:
#             blogs = db.query(models.Blog).filter(models.Blog.cat == cat).all()
#             if not blogs:
#                 raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"No blogs found in category {cat}")
#         else:
#             blogs = db.query(models.Blog).all()
#         return blogs
#     except Exception as e:
#         print(f"Error: {e}")
#         raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal Server Error")



# CREATE POST (with image)
# TODO añadir validaciones y raise excepciones      ///// ***********************AÑADIR  user id y date?????????????

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
    file: UploadFile = File(...),
    db: Session = Depends(get_db)
):
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
    
    try:
        user_id=1  # Added user id manually for testing
        # new_blog = models.Blog(title=title, desc=desc, cat=cat, image=file_location, user_id=user_id)
        # db.add(new_blog)
        # db.commit()
        # db.refresh(new_blog)
        
        # return new_blog
        return blog.create_blog(db, title, desc, cat, file_location, user_id)
    except Exception as e:
        logger.error(f"Error creating blog: {e}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal server error")


##******************************end of create blog*****************************************


# GET ONE LOCATION BLOG

@router.get("/{id}", status_code=200, response_model=schemas.ShowBlog)
def get_one(id:int, db:Session= Depends(database.get_db)):
    # blog = db.query(models.Blog).filter(models.Blog.id == id).first()
    # if not blog:
    #     raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Blog with id {id} is not available")
    # return blog
    return blog.get_one_blog(id, db)



# DELETE ONE LOCATON BLOG

@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete(id, db: Session = Depends(get_db)):
    # blog = db.query(models.Blog).filter(models.Blog.id ==id)
    # if not blog.first():
    #     raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Blog with id {id} is not available")
    # blog.delete(synchronize_session=False)
    # db.commit()
    # return "The blog was deleted successfully"
    return blog.delete_blog(id, db)



# UPDATE ONE LOCATION BLOG

# TODO añadir validaciones y raise excepciones

# No need ANY DATE pero sí USER ID!!!!!!!!!!!!!!!!!!!!!!!!!!
# condición de id y udi para editar
@router.put("/update_blog/{blog_id}", status_code=status.HTTP_200_OK, response_model=schemas.ShowBlog)
async def update_blog(blog_id: int, title: Optional[str] = Form(None), desc: Optional[str] = Form(None), cat: Optional[str] = Form(None), image: Optional[UploadFile] = None, db: Session = Depends(get_db)):
    # blog_to_update = db.query(models.Blog).filter(models.Blog.id == blog_id).first()
    
    # if not blog_to_update:
    #     raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Blog not found")
    
    # if title is not None:
    #     blog_to_update.title = title
    # if desc is not None:
    #     blog_to_update.desc = desc
    # if cat is not None:
    #     blog_to_update.cat = cat
    file_location = None  # new thing
    if image is not None:
        contents = await image.read()
        file_location = f"uploadImage/{image.filename}"
        with open(file_location, "wb") as buffer:
            buffer.write(contents)
        # blog_to_update.image = file_location
    
    # db.commit()
    # db.refresh(blog_to_update)
    
    # return blog_to_update
    return blog.update_blog(blog_id, db, title, desc, cat, file_location)
