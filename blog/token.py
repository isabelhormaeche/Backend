from datetime import datetime, timedelta
from jose import  jwt, JWTError
from dotenv import load_dotenv
import os
from . import schemas

load_dotenv()

SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM")
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES"))


# CREATE ACCESS TOKEN:
def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


# VERIFY THE TOKEN:
def verify_token(token:str,credentials_exception):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email: str = payload.get("sub")
        user_id: int = payload.get("user_id")
        # if email is None:
        if email is None or user_id is None:
            raise credentials_exception
        # token_data = schemas.TokenData(email=email)
        token_data = schemas.TokenData(email=email, user_id=user_id)
        return token_data
    except JWTError:
        raise credentials_exception
