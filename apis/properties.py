from datetime import datetime
import logging
from xmlrpc.client import boolean
from fastapi import APIRouter, HTTPException, Depends, status
from pydantic import BaseModel
from typing import Annotated, List, Optional

import sqlalchemy

import models
from database import engine, SessionLocal
from sqlalchemy.orm import Session
from sqlalchemy import Float, select


router = APIRouter()

class Amenities(BaseModel):
    hasGym: bool
    hasPool: bool
    hasBBQPit: bool
    hasTennisCourt: bool
    hasBasketballCourt: bool
    hasParking: bool

class MapData(BaseModel):
    latitude: float
    longtitude: float

class NearestMRTStation(BaseModel):
    station: str
    distanceInMinutes: int

class NearestBusStop(BaseModel):
    station: str
    distanceInMinutes: int

class ComunalSpacesImage(BaseModel):
    link: str
    alt: str

class PropertyBase(BaseModel):
    name: str
    address: str
    district: str
    postalCode: str
    description1: str
    description2: str
    heroImageLink: str
    communalSpacesImages: List[ComunalSpacesImage]
    numberOfBathrooms: int
    amenities: Amenities
    pricePerMonth: float
    tenancyEndDate: datetime
    utilityCap: int
    wifi: str
    wifiPassword: str
    passcode: str
    nearestMRTStation: List[NearestMRTStation]
    nearestBusStop: List[NearestBusStop]
    mapData: MapData
    floorPlanImageLink: str
    videoLink: str

class FormProperties(BaseModel):
    id: int
    name: str
    class Config:
        orm_mode = True

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

db_dependency = Annotated[Session, Depends(get_db)]

@router.get("/form-properties/", response_model=List[FormProperties], status_code=status.HTTP_200_OK)
async def get_form_properties(db: db_dependency):
    stmt = select(models.Property)
    result = db.execute(stmt)
    formProperties = result.scalars().all()
    return formProperties

@router.get("/properties/", status_code=status.HTTP_200_OK)
async def get_properties(db: db_dependency):
    stmt = select(models.Property)
    result = db.execute(stmt)
    properties = result.scalars().all()
    return properties

@router.get("/properties/{property_id}", status_code=status.HTTP_200_OK)
async def get_property_by_id(property_id: int, db: Annotated[Session, Depends(get_db)]):
    db_property = db.query(models.Property).filter(models.Property.id == property_id).first()
    if db_property is None:
        raise HTTPException(status_code=404, detail="Property not found")
    # db_property.communalSpacesImages = db.query(models.CommunalSpaceImage).filter(models.CommunalSpaceImage.propertyId == property_id).all()
    return db_property

@router.post("/properties/", status_code=status.HTTP_201_CREATED)
async def create_property(property:PropertyBase, db: db_dependency):
    try:
        db_property = models.Property(**property.dict())
        db.add(db_property)
        
        db.commit()
        
        return {"message": "Property created successfully", "property_id": db_property.id}
    except sqlalchemy.exc.SQLAlchemyError as e:
        db.rollback()
        logging.error(f"An error occurred: {e}")
        raise HTTPException(status_code=status.HTTP_422, detail=str(e))

@router.put("/properties/{property_id}", status_code=status.HTTP_200_OK)
async def update_property(property_id: int, property: PropertyBase, db: db_dependency):
    try:
        db_property = db.query(models.Property).filter(models.Property.id == property_id).first()
        
        if not db_property:
            raise HTTPException(status_code=404, detail="Room not found")
        
        for attr, value in property.dict(exclude_unset=True).items():
            setattr(db_property, attr, value)

        db.commit()

        return {"message": "Property updated successfully", "property": property}
    except sqlalchemy.exc.SQLAlchemyError as e:
        db.rollback()
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))

    return db_property


@router.delete("/properties/{property_id}",status_code=status.HTTP_200_OK)
async def delete_property(property_id: int, db:db_dependency):
    db_property = db.query(models.Property).filter(models.Property.id == property_id).first()
    if db_property is None:
        raise HTTPException(status_code=404, detail='Room not found')
    db.delete(db_property)
    db.commit()

@router.delete("/properties/communal_space_images/{communal_space_id}",status_code=status.HTTP_200_OK)
async def delete_communal_image(communal_space_id: int, db:db_dependency):
    db_comprop = db.query(models.CommunalSpaceImage).filter(models.CommunalSpaceImage.id == communal_space_id).first()
    if db_comprop is None:
        raise HTTPException(status_code=404, detail='Image not found')
    db.delete(db_comprop)
    db.commit()