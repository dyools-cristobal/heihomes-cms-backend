from uu import encode
from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel
from sqlalchemy.orm import Session
from database import engine, SessionLocal
import jwt
import datetime
import models
from dotenv import load_dotenv


router = APIRouter()

class User(BaseModel):
    username: str
    password: str

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

SECRET_KEY = "heihomesisdabes"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30
# from apis.users import get_user

@router.post("/auth/login")
async def login(user: User, db: Session = Depends(get_db)):
    # Fetch user details from the get_user API
    db_user = db.query(models.User).filter(models.User.username == user.username).first()
    if not db_user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    
    encoded_password = jwt.encode({"password": user.password}, SECRET_KEY, algorithm=ALGORITHM) # type: ignore
    
    if db_user and db_user.password == encoded_password: # type: ignore
        payload = {
            'user_id': db_user.id, # type: ignore
            'username': db_user.username, # type: ignore
            'exp': datetime.datetime.utcnow() + datetime.timedelta(days=1)  # Expiration time
        }
        token = jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)
        return {"message": "Login successful", "username": db_user.username, "token": token} # type: ignore
    else:
        raise HTTPException(status_code=401, detail="Invalid username or password")