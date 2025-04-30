from pydantic import BaseModel
from typing import List, Optional

class HotelAccommodationSchema(BaseModel):
    name: str
    location: str

class TransferSchema(BaseModel):
    from_location: str
    to_location: str
    mode: str

class ActivitySchema(BaseModel):
    name: str
    description: str
    location: str

class ItineraryDayCreateSchema(BaseModel):
    day_number: int
    hotel_accommodations: List[HotelAccommodationSchema]
    transfers: List[TransferSchema]
    activities: List[ActivitySchema]

class ItineraryCreateSchema(BaseModel):
    title: str
    duration: int
    region: str
    days: List[ItineraryDayCreateSchema]

class ItineraryResponseSchema(BaseModel):
    id: int
    title: str
    duration: int
    region: str

    class Config:
        orm_mode = True
