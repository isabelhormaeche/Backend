from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from .. import schemas, database, models, token
from sqlalchemy.orm import Session
from ..hashing import Hash

router = APIRouter(tags=['Authentication'])

@router.post('/api/login')
def login(request:OAuth2PasswordRequestForm = Depends(), db: Session = Depends(database.get_db)):
    try:
        user = db.query(models.User).filter(models.User.email == request.username).first()
        # CHECK USER    
        if not user:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Invalid Credentials")
        
        # CHECK PASSWORD
        # Compare request.password(plaintext password provided by the user) and user.password (hash stored in the database)
        if not Hash.verify(request.password, user.password):
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Incorrect password")
        
        # if everythin OK then create TOKEN
        # access_token = token.create_access_token(data={"sub": user.email})
        access_token = token.create_access_token(data={"sub": user.email, "user_id": user.id})
        return {"access_token": access_token, "token_type": "bearer"}
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))
    

    # Added "user id" to the payload:
    # Generating a JWT token that includes the user's ID, 
    # React frontend can store and use this ID as needed. 
    # This will allow me to maintain the user's session and 
    # access their information.
    # https://jwt.io/ for checking inside payload data