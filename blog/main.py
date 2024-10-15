from fastapi import FastAPI
from . import models
from .database import engine
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from .routers import blog, user
# import os


app = FastAPI()

# TODO Change ORIGIN when send to production *************************
origin = [
    # 'http://localhost:3000'
    ("*")
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origin,
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*']
    )


# Configuration for serving static files: allows files in the uploadImage directory to be accessible via the /uploadImage URL.
app.mount("/uploadImage", StaticFiles(directory="uploadImage"), name="uploadImage")


# DELETE the blog.db file if any (to clean up and begin again creating the tables):
# db_path = "blog.db"
# if os.path.exists(db_path):
#     os.remove(db_path)


# Create all the tables 
models.Base.metadata.create_all(engine)

app.include_router(blog.router)
app.include_router(user.router)





# *************************CLEAN UP LATER from here ********************


# def get_db():
#     db = SessionLocal()
#     try:
#         yield db
#     finally:
#         db.close()

    
# UPLOAD image with FastAPI

# https://fastapi.tiangolo.com/tutorial/request-files/#file-parameters-with-uploadfile
# https://youtu.be/m6Ma6B6VlFs?feature=shared
# https://galaxyofai.com/how-to-send-images-to-python-fastapi-using-postman/

# # Allowed image types and max size:
# ALLOWED_IMAGE_TYPES = ["image/jpeg", "image/png"]
# MAX_IMAGE_SIZE = 2 * 1024 * 1024  # 2 MB

# # logger configuration:
# logging.basicConfig(level=logging.INFO)
# logger = logging.getLogger(__name__)

# UPLOAD IMAGE

# @app.post("/api/upload_image_one", status_code=status.HTTP_201_CREATED)
# async def upload_image(file: UploadFile = File(...)):
#     logger.info(f"Received file: {file.filename}")
#     if file.content_type not in ALLOWED_IMAGE_TYPES:
#         logger.error("Invalid image type")
#         raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid image type. Only JPEG and PNG are allowed.")
    
#     contents = await file.read()
#     if len(contents) > MAX_IMAGE_SIZE:
#         logger.error("Image size exceeds the maximum limit")
#         raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Image size exceeds the maximum limit of 2 MB.")
    
#     file_location = f"uploadImage/{file.filename}"
#     try:
#         with open(file_location, "wb") as buffer:
#             buffer.write(contents)
#         logger.info(f"File saved at {file_location}")
#     except Exception as e:
#         logger.error(f"Error saving file: {e}")
#         raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal server error")
    
#     return {"file_location": file_location}

# ******************CREATE FOLDER FOR ---> IMAGES****************************
# if not os.path.exists('uploadImage'):
#     os.makedirs('uploadImage')


# # NEW ENDPOINT CREATE POST WITH IMAGE

# @app.post("/api/create_blog_with_image", status_code=status.HTTP_201_CREATED, response_model=schemas.ShowBlog, tags=["blogs"])
# async def upload_image(
#     title: str = Form(...),
#     desc: str = Form(...),
#     cat: str = Form(...),
#     file: UploadFile = File(...),
#     db: Session = Depends(get_db)
# ):
#     logger.info(f"Received file: {file.filename}")
#     if file.content_type not in ALLOWED_IMAGE_TYPES:
#         logger.error("Invalid image type")
#         raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid image type. Only JPEG and PNG are allowed.")
    
#     contents = await file.read()
#     if len(contents) > MAX_IMAGE_SIZE:
#         logger.error("Image size exceeds the maximum limit")
#         raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Image size exceeds the maximum limit of 2 MB.")
    
#     file_location = f"uploadImage/{file.filename}"
#     try:
#         with open(file_location, "wb") as buffer:
#             buffer.write(contents)
#         logger.info(f"File saved at {file_location}")
#     except Exception as e:
#         logger.error(f"Error saving file: {e}")
#         raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal server error")
    
#     try:
#         # Added user id manually for testing
#         user_id=1  
#         new_blog = models.Blog(title=title, desc=desc, cat=cat, image=file_location, user_id=user_id)
#         db.add(new_blog)
#         db.commit()
#         db.refresh(new_blog)
        
#         return new_blog
#     except Exception as e:
#         logger.error(f"Error creating blog: {e}")
#         raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal server error")




# # Merging BOTH: Get all location blogs by category(if any) if none get all:

# @app.get("/api/blog", response_model=List[schemas.ShowBlog], tags=["blogs"])
# def get_blogs(cat: Optional[str] = None, db: Session = Depends(get_db)):
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



# # Get one location blog

# @app.get("/api/blog/{id}", status_code=200, response_model=schemas.ShowBlog, tags=["blogs"])
# def get_one(id, response: Response, db:Session= Depends(get_db)):
#     blog = db.query(models.Blog).filter(models.Blog.id == id).first()
#     if not blog:
#         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Blog with id {id} is not available")
#     return blog



# # Delete one location blog

# @app.delete("/api/blog/{id}", status_code=status.HTTP_204_NO_CONTENT, tags=["blogs"])
# def delete(id, db: Session = Depends(get_db)):
#     blog = db.query(models.Blog).filter(models.Blog.id ==id)
#     if not blog.first():
#         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Blog with id {id} is not available")
#     blog.delete(synchronize_session=False)
#     db.commit()
#     return "The blog was deleted successfully"



# # Update one location blog

# # TODO añadir validaciones y raise excepciones

# # No need ANY DATE pero sí USER ID!!!!!!!!!!!!!!!!!!!!!!!!!!
# # condición de id y udi para editar
# @app.put("/api/update_blog/{blog_id}", status_code=status.HTTP_200_OK, response_model=schemas.ShowBlog, tags=["blogs"])
# async def update_blog(blog_id: int, title: Optional[str] = Form(None), desc: Optional[str] = Form(None), cat: Optional[str] = Form(None), image: Optional[UploadFile] = None, db: Session = Depends(get_db)):
#     blog_to_update = db.query(models.Blog).filter(models.Blog.id == blog_id).first()
    
#     if not blog_to_update:
#         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Blog not found")
    
#     if title is not None:
#         blog_to_update.title = title
#     if desc is not None:
#         blog_to_update.desc = desc
#     if cat is not None:
#         blog_to_update.cat = cat
#     if image is not None:
#         contents = await image.read()
#         file_location = f"uploadImage/{image.filename}"
#         with open(file_location, "wb") as buffer:
#             buffer.write(contents)
#         blog_to_update.image = file_location
    
#     db.commit()
#     db.refresh(blog_to_update)
    
#     return blog_to_update



# Delete ***********ALL********** the blogs (TODO: borrar luego porque es para desarrollo solo) ********************************

# @app.delete("/api/blogs", status_code=status.HTTP_204_NO_CONTENT, tags=["blogs"])
# def delete_all_blogs(db: Session = Depends(get_db)):
#     db.query(models.Blog).delete()
#     db.commit()
#     return {"detail": "All blogs deleted successfully"}


# *******************ENDPOINTS USER ****************************************

# # CREATE USER 
# @app.post("/api/user", response_model=schemas.ShowUser, tags=["users"])
# def create_user(request: schemas.User, db: Session = Depends(get_db)):
#      hashed_password = Hash.bcrypt(request.password)
#      new_user = models.User(name=request.name, email=request.email, password=hashed_password)
#      db.add(new_user)
#      db.commit()
#      db.refresh(new_user)
#      return new_user


# # GET USER
# @app.get("/api/user/{id}", response_model=schemas.ShowUser, tags=["users"])
# def get_user(id:int, db: Session = Depends(get_db)):
#     user = db.query(models.User).filter(models.User.id == id).first()
#     if not user:
#         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"User with id {id} is not available")
#     return user
             

