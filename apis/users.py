from decimal import Decimal
from fastapi import APIRouter, HTTPException, Depends, status
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

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

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

def reg_user(db: Session, user:UserBase):
    hashed_password = pwd_context.hash(user.password)
    db_user = models.User(username=user.username, password=hashed_password)
    db.add(db_user)
    db.commit()
    return "User created successfully!"

# create user
@router.post("/users/create/", status_code=status.HTTP_201_CREATED)
async def create_user(user: UserBase, db: db_dependency):
    db_user = get_user_by_username(db, username=user.username)
    if db_user:
        raise HTTPException(status_code=400, detail="User already exists")
    return reg_user(db=db, user=user)


    # db_user = models.User(**user.dict())
    # db.add(db_user)
    # db.commit()

# update user
@router.put("/users/{user_id}", status_code=status.HTTP_200_OK)
async def update_user(user_id: int, user: UserBase, db: db_dependency):
    # Retrieve the user from the database
    db_user = db.query(models.User).filter(models.User.id == user_id).first()
    
    # Check if the user exists
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")
    
    # Update user attributes
    for attr, value in user.dict().items():
        setattr(db_user, attr, value)
    
    # Commit changes to the database
    db.commit()
    
    return db_user

# get user by id
@router.get("/users/{user_id}", status_code=status.HTTP_200_OK)
async def read_user(user_id: int, db: db_dependency):
    user = db.query(models.User).filter(models.User.id == user_id).first()
    if user is None:
        raise HTTPException(status_code=404, detail='User not found')
    return user