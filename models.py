from decimal import Decimal
from tkinter.font import BOLD
from fastapi import FastAPI
from pydantic import BaseModel
from sqlalchemy import ARRAY, JSON, Boolean, Column, ForeignKey, Integer, String, Float
from sqlalchemy.orm import relationship
# from sqlalchemy.ext.declarative import declarative_base
from database import Base

class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, index=True)
    roleId = Column(Integer)
    username = Column(String(50), unique=True)
    password = Column(String(50))

class Amenity(Base):
    __tablename__ = 'amenities'

    id = Column(Integer, primary_key=True, index=True)
    roomId = Column(Integer, ForeignKey('rooms.id'))
    name = Column(String(50))
    fee = Column(Float)

class Role(Base):
    __tablename__ = 'roles'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(50))
    description = Column(String(50))

class Room(Base):
    __tablename__ = 'rooms'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(50))
    unitId = Column(Integer)
    roomType = Column(String(50))
    squareFootage = Column(Integer)
    bedType = Column(String(50))
    closet = Column(Boolean)
    attachedBathroom = Column(Boolean)
    bathtub = Column(Boolean)
    desk = Column(Boolean)
    details1 = Column(String(500))
    details2 = Column(String(500))
    coupleRoom = Column(Boolean)
    available = Column(Boolean)
    nextAvailabilityDate = Column(String(50))
    pricePerMonth = Column(Float)
    promoPrice = Column(Float)
    promoPeriodFrom = Column(String(50))
    promoPeriodTo = Column(String(50))
    nearestMRT = Column(JSON)
    mapData = Column(JSON)
    floorPlanLink = Column(String(150))
    carouselImages = Column(JSON)