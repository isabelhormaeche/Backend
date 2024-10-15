from fastapi import APIRouter
from fastapi import APIRouter, Depends, status, HTTPException
from .. import schemas, database, models
from sqlalchemy.orm import Session
from ..hashing import Hash


router = APIRouter(
    prefix="/user",
    tags=['Users']
)

get_db = database.get_db

# CREATE USER 
@router.post("/api/user", response_model=schemas.ShowUser)
def create_user(request: schemas.User, db: Session = Depends(get_db)):
     hashed_password = Hash.bcrypt(request.password)
     new_user = models.User(name=request.name, email=request.email, password=hashed_password)
     db.add(new_user)
     db.commit()
     db.refresh(new_user)
     return new_user


# GET USER
@router.get("/api/user/{id}", response_model=schemas.ShowUser)
def get_user(id:int, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"User with id {id} is not available")
    return user
             
