from datetime import datetime
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


router = APIRouter()

class Amenities(BaseModel):
    amenities: List[int]

class MapData(BaseModel):
    latitude: float
    longtitude: float

class NearestMRT(BaseModel):
    station: str
    distanceInMinutes: int

class CarouselImages(BaseModel):
    image: str
    alt: str

class RoomBase(BaseModel):
    name: str
    unitId: int
    roomType: str
    squareFootage: int
    bedType: str
    closet: bool
    attachedBathroom: bool
    bathtub: bool
    desk: bool
    details1: str
    details2: str
    coupleRoom: bool
    available: bool
    nextAvailabilityDate: str
    pricePerMonth: float
    promoPrice: float
    promoPeriodFrom: str
    promoPeriodTo: str
    nearestMRT: List[NearestMRT]
    mapData: MapData
    floorPlanLink: str
    carouselImages: List[CarouselImages]
    


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

db_dependency = Annotated[Session, Depends(get_db)]

@router.get("/rooms/", status_code=status.HTTP_200_OK)
async def get_room(db: db_dependency):
    stmt = select(models.Room)
    result = db.execute(stmt)
    rooms = result.scalars().all()
    return rooms

@router.get("/rooms/{room_id}", response_model=RoomBase)
async def get_room_by_id(room_id: int, db: Annotated[Session, Depends(get_db)]):
    db_room = db.query(models.Room).filter(models.Room.id == room_id).first()
    if db_room is None:
        raise HTTPException(status_code=404, detail="Room not found")
    return db_room

@router.post("/rooms/", status_code=status.HTTP_201_CREATED)
async def create_room(room:RoomBase, db: db_dependency):
    try:
        db_room = models.Room(**room.dict())
        db.add(db_room)
        db.commit()
        return {"message": "Room created successfully", "room_id": db_room.id}
    except sqlalchemy.exc.SQLAlchemyError as e:
        db.rollback()
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail=str(e))


@router.put("/rooms/{room_id}", status_code=status.HTTP_200_OK)
async def update_room(room_id: int, room: RoomBase, db: db_dependency):
    # Retrieve the room from the database
    db_room = db.query(models.Room).filter(models.Room.id == room_id).first()
    
    # Check if the user exists
    if not db_room:
        raise HTTPException(status_code=404, detail="Room not found")
    
    # Update user attributes
    for attr, value in room.dict().items():
        setattr(db_room, attr, value)
    
    # Commit changes to the database
    db.commit()
    
    return db_room


@router.delete("/rooms/{room_id}",status_code=status.HTTP_200_OK)
async def delete_room(room_id: int, db:db_dependency):
    db_room = db.query(models.Room).filter(models.Room.id == room_id).first()
    if db_room is None:
        raise HTTPException(status_code=404, detail='Room not found')
    db.delete(db_room)
    db.commit()