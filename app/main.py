from fastapi import FastAPI
from . import models
from .database import engine
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from .routers import blog, user, auth

app = FastAPI()

app.mount("/static", StaticFiles(directory="app/static"), name="static")

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

@app.get("/")
def read_root():
    return {"message": "Welcome to my Film Locations FastAPI application!"}

app.include_router(auth.router)
app.include_router(blog.router)
app.include_router(user.router)
