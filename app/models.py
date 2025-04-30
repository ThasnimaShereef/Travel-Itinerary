from sqlalchemy import Column, Integer, String, ForeignKey, Date, Text
from sqlalchemy.orm import relationship, declarative_base

Base = declarative_base()

class Itinerary(Base):
    __tablename__ = 'itineraries'

    id = Column(Integer, primary_key=True)
    title = Column(String, nullable=False)
    duration = Column(Integer, nullable=False)  
    region = Column(String, nullable=False)     

    days = relationship("ItineraryDay", back_populates="itinerary", cascade="all, delete-orphan")


class ItineraryDay(Base):
    __tablename__ = 'itinerary_days'

    id = Column(Integer, primary_key=True)
    day_number = Column(Integer, nullable=False)
    itinerary_id = Column(Integer, ForeignKey("itineraries.id"), nullable=False)

    itinerary = relationship("Itinerary", back_populates="days")
    accommodations = relationship("HotelAccommodation", back_populates="day", cascade="all, delete-orphan")
    transfers = relationship("Transfer", back_populates="day", cascade="all, delete-orphan")
    activities = relationship("Activity", back_populates="day", cascade="all, delete-orphan")


class HotelAccommodation(Base):
    __tablename__ = 'accommodations'

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    location = Column(String, nullable=False)
    day_id = Column(Integer, ForeignKey("itinerary_days.id"), nullable=False)

    day = relationship("ItineraryDay", back_populates="accommodations")


class Transfer(Base):
    __tablename__ = 'transfers'

    id = Column(Integer, primary_key=True)
    from_location = Column(String, nullable=False)
    to_location = Column(String, nullable=False)
    mode = Column(String, nullable=False)  
    day_id = Column(Integer, ForeignKey("itinerary_days.id"), nullable=False)

    day = relationship("ItineraryDay", back_populates="transfers")


class Activity(Base):
    __tablename__ = 'activities'

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    description = Column(Text)
    location = Column(String)
    day_id = Column(Integer, ForeignKey("itinerary_days.id"), nullable=False)

    day = relationship("ItineraryDay", back_populates="activities")


class RecommendedItinerary(Base):
    __tablename__ = 'recommended_itineraries'

    id = Column(Integer, primary_key=True)
    title = Column(String, nullable=False)
    duration = Column(Integer, nullable=False)
    content = Column(Text, nullable=False)  
    region = Column(String, nullable=False)
