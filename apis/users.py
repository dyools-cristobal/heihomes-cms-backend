import os
from fastapi import APIRouter, Depends, HTTPException, status
import jwt
from pydantic import BaseModel
from typing import Annotated
from database import engine, SessionLocal
from sqlalchemy.orm import Session
import models
from dotenv import load_dotenv


router = APIRouter()

class UserBase(BaseModel):
    username: str
    roleId: int
    password: str

class UserResponse(BaseModel):
    username: str
    roleId: int

# pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Your JWT secret and algorithm
SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM")
ACCESS_TOKEN_EXPIRE_MINUTES = os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES")

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

db_dependency = Annotated[Session, Depends(get_db)]


@router.post("/users/", status_code=status.HTTP_201_CREATED)
async def create_user(user: UserBase, db: Session = Depends(get_db)):
    encoded_password = jwt.encode({"password": user.password}, SECRET_KEY, algorithm=ALGORITHM)
    db_user = models.User(username=user.username, roleId=user.roleId, password=encoded_password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

@router.put("/users/{username}/password", status_code=status.HTTP_200_OK)
async def update_user_password(username: str, new_password: str, db: Session = Depends(get_db)):
    db_user = db.query(models.User).filter(models.User.username == username).first()
    if not db_user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    
    encoded_password = jwt.encode({"password": new_password}, SECRET_KEY, algorithm=ALGORITHM)
    db_user.password = encoded_password # type: ignore
    db.commit()
    db.refresh(db_user)
    return {"msg": "Password updated successfully"}

@router.get("/users/{username}", status_code=status.HTTP_302_FOUND)
async def get_user(username: str, db: Session = Depends(get_db)):
    db_user = db.query(models.User).filter(models.User.username == username).first()
    if not db_user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    
    return db_user
