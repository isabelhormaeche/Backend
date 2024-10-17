from fastapi import FastAPI
from . import models
from .database import engine
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from .routers import blog, user, auth

app = FastAPI()


origin = [
    
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



# Create all the tables 
models.Base.metadata.create_all(engine)

app.include_router(auth.router)
app.include_router(blog.router)
app.include_router(user.router)
