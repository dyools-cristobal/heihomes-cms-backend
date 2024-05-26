from decimal import Decimal
from fastapi import APIRouter, Depends
from pydantic import BaseModel
from typing import Annotated, Optional 
import models
from database import engine, SessionLocal
from sqlalchemy.orm import Session
from passlib.context import CryptContext


router = APIRouter()

class UserBase(BaseModel):
    username: str
    role_id: int
    password: str

# pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Your JWT secret and algorithm
SECRET_KEY = "your_secret_key"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

db_dependency = Annotated[Session, Depends(get_db)]

def get_user_by_username(db: Session, username: str):
    return db.query(models.User).filter(models.User.username == username).first()
