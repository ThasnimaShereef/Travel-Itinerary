from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from app.database import get_db
from app import models, schemas

router = APIRouter()

@router.post("/itineraries", response_model=schemas.ItineraryResponseSchema)
def create_itinerary(itinerary: schemas.ItineraryCreateSchema, db: Session = Depends(get_db)):
    db_itinerary = models.Itinerary(
        title=itinerary.title,
        duration=itinerary.duration,
        region=itinerary.region
    )
    db.add(db_itinerary)
    db.commit()
    db.refresh(db_itinerary)

    for day_data in itinerary.days:
        day = models.ItineraryDay(
            day_number=day_data.day_number,
            itinerary_id=db_itinerary.id
        )
        db.add(day)
        db.commit()
        db.refresh(day)

        for hotel in day_data.hotel_accommodations:
            db.add(models.HotelAccommodation(name=hotel.name, location=hotel.location, day_id=day.id))

        for transfer in day_data.transfers:
            db.add(models.Transfer(from_location=transfer.from_location, to_location=transfer.to_location, mode=transfer.mode, day_id=day.id))

        for activity in day_data.activities:
            db.add(models.Activity(name=activity.name, description=activity.description, location=activity.location, day_id=day.id))

    db.commit()
    return db_itinerary

@router.get("/itineraries", response_model=List[schemas.ItineraryResponseSchema])
def get_all_itineraries(db: Session = Depends(get_db)):
    return db.query(models.Itinerary).all()

@router.get("/itineraries/{itinerary_id}")
def get_itinerary_details(itinerary_id: int, db: Session = Depends(get_db)):
    itinerary = db.query(models.Itinerary).filter(models.Itinerary.id == itinerary_id).first()
    if not itinerary:
        raise HTTPException(status_code=404, detail="Itinerary not found")

    response = {
        "id": itinerary.id,
        "title": itinerary.title,
        "duration": itinerary.duration,
        "region": itinerary.region,
        "days": []
    }

    for day in itinerary.days:
        response["days"].append({
            "day_number": day.day_number,
            "hotel_accommodations": [{"name": h.name, "location": h.location} for h in day.hotel_accommodations],
            "transfers": [{"from_location": t.from_location, "to_location": t.to_location, "mode": t.mode} for t in day.transfers],
            "activities": [{"name": a.name, "description": a.description, "location": a.location} for a in day.activities]
        })

    return response
