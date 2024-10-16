from fastapi import status, HTTPException
from sqlalchemy.orm import Session
from .. import models, schemas
from ..hashing import Hash



# CREATE USER 
def create_user(request: schemas.User, db: Session):
    # CHECK EXISTING USER
    existing_user = db.query(models.User).filter(models.User.email == request.email).first()
    if existing_user:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Email already registered")


    try:
        hashed_password = Hash.bcrypt(request.password)
        new_user = models.User(name=request.name, email=request.email, password=hashed_password)
        db.add(new_user)
        db.commit()
        db.refresh(new_user)
        return new_user
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))
    


# GET USER 
def get_user(id: int, db: Session):
    user = db.query(models.User).filter(models.User.id == id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"User with id {id} is not available")
    return user
