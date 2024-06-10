from sqlalchemy import ARRAY, JSON, Boolean, Column, DateTime, ForeignKey, Integer, String, Float
from sqlalchemy.orm import relationship
from apis.properties import NearestMRTStation
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

class Property(Base):
    __tablename__ = 'properties'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(50))
    address = Column(String(150))
    district = Column(String(150))
    postalCode = Column(String(20))
    description1 = Column(String(500))
    description2 = Column(String(500), nullable=True)
    heroImageLink = Column(String(500), nullable=True)
    communalSpacesImages = Column(JSON, nullable=True)
    numberOfBathrooms = Column(Integer, nullable=True)
    amenities = Column(JSON, nullable=True)
    pricePerMonth = Column(Float, nullable=True)
    tenancyEndDate = Column(DateTime, nullable=True)
    utilityCap = Column(Integer, nullable=True)
    wifi = Column(String(50))
    wifiPassword = Column(String(50))
    passcode = Column(String(50))
    nearestMRTStation = Column(JSON, nullable=True)
    nearestBusStop = Column(JSON, nullable=True)
    mapData = Column(JSON, nullable=True)
    floorPlanImageLink = Column(String(500), nullable=True)
    videoLink = Column(String(500), nullable=True)
    

class CommunalSpaceImage(Base):
    __tablename__ = 'communal_space_images'

    id = Column(Integer, primary_key=True, index=True)
    propertyId = Column(Integer, ForeignKey('properties.id'))
    link = Column(String(500))
    alt = Column(String(500))