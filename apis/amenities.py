import string
from xmlrpc.client import boolean
from fastapi import APIRouter, HTTPException, Depends, status
from pydantic import BaseModel
from typing import Annotated, List, Optional

import sqlalchemy

import models
from database import engine, SessionLocal
from sqlalchemy.orm import Session
from sqlalchemy import Float, select
from passlib.context import CryptContext


router = APIRouter()

class AmenityBase(BaseModel):
    name: str
    fee: float

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

db_dependency = Annotated[Session, Depends(get_db)]

@router.get("/amenities/", status_code=status.HTTP_200_OK)
async def get_amenities(db: db_dependency):
    stmt = select(models.Amenity)
    result = db.execute(stmt)
    formProperties = result.scalars().all()
    return formProperties

@router.get("/amenities/{amenity_id}", status_code=status.HTTP_200_OK)
async def get_amenity_by_id(amenity_id: int, db: Annotated[Session, Depends(get_db)]):
    db_amenity = db.query(models.Amenity).filter(models.Amenity.id == amenity_id).first()
    if db_amenity is None:
        raise HTTPException(status_code=404, detail="Amenity not found")
    return db_amenity

@router.post("/amenities/", status_code=status.HTTP_201_CREATED)
async def create_amenity(amenity:AmenityBase, db: db_dependency):
    try:
        db_amenity = models.Amenity(**amenity.dict())
        db.add(db_amenity)
        db.commit()
        return {"message": "Amenity created successfully", "amenity_id": db_amenity.id}
    except sqlalchemy.exc.SQLAlchemyError as e:
        db.rollback()
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))

@router.put("/amenities/{amenity_id}", status_code=status.HTTP_200_OK)
async def update_amenity(amenity_id: int, amenity: AmenityBase, db: db_dependency):
    # Retrieve the room from the database
    db_amenity = db.query(models.Amenity).filter(models.Amenity.id == amenity_id).first()
    
    # Check if the user exists
    if not db_amenity:
        raise HTTPException(status_code=404, detail="Amenity not found")
    
    # Update user attributes
    for attr, value in amenity.dict().items():
        setattr(db_amenity, attr, value)
    
    # Commit changes to the database
    db.commit()
    
    return db_amenity

@router.delete("/amenities/{property_id}",status_code=status.HTTP_200_OK)
async def delete_property(property_id: int, db:db_dependency):
    db_property = db.query(models.Property).filter(models.Property.id == property_id).first()
    if db_property is None:
        raise HTTPException(status_code=404, detail='Room not found')
    db.delete(db_property)
    db.commit()