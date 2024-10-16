from fastapi import APIRouter, Depends, HTTPException, status
from .. import schemas, database, models, token
from sqlalchemy.orm import Session
from ..hashing import Hash

router = APIRouter(tags=['Authentication'])

@router.post('/login')
def login(request:schemas.Login, db: Session = Depends(database.get_db)):
    try:
        user = db.query(models.User).filter(models.User.email == request.username).first()
        if not user:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Invalid Credentials")
        
        # Compare request.password(plaintext password provided by the user) and user.password (hash stored in the database)
        if not Hash.verify(request.password, user.password):
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Incorrect password")
        
        # if everythin OK then create TOKEN
        access_token = token.create_access_token(data={"sub": user.email})
        return {"access_token": access_token, "token_type": "bearer"}
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))