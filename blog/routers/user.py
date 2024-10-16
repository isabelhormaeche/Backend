from fastapi import APIRouter
from fastapi import APIRouter, Depends
from .. import schemas, database
from sqlalchemy.orm import Session
# from ..hashing import Hash
from ..crud import user


router = APIRouter(
    prefix="/api/users",
    tags=['Users']
)

get_db = database.get_db

# CREATE USER 
@router.post("/", response_model=schemas.ShowUser)
def create_user(request: schemas.User, db: Session = Depends(get_db)):
     return user.create_user(request, db)


# GET USER
@router.get("/{id}", response_model=schemas.ShowUser)
def get_user(id:int, db: Session = Depends(get_db)):
    return user.get_user(id, db)
             
