from .database import SessionLocal, init_db
from .models import Itinerary, ItineraryDay, HotelAccommodation, Transfer, Activity, RecommendedItinerary
import json

def seed_sample_data():
    init_db()
    db = SessionLocal()

    # Clear existing data
    db.query(RecommendedItinerary).delete()
    db.query(Activity).delete()
    db.query(Transfer).delete()
    db.query(HotelAccommodation).delete()
    db.query(ItineraryDay).delete()
    db.query(Itinerary).delete()
    db.commit()

    # ----------------------
    # Phuket 3-Night Trip
    # ----------------------
    phuket_trip = Itinerary(title="Phuket Getaway", duration=3, region="Phuket")
    db.add(phuket_trip)
    db.commit()

    for day in range(1, 4):
        day_obj = ItineraryDay(day_number=day, itinerary_id=phuket_trip.id)
        db.add(day_obj)
        db.commit()

        db.add_all([
            HotelAccommodation(name=f"Hotel Paradise Day {day}", location="Phuket", day_id=day_obj.id),
            Activity(name=f"Beach Day {day}", description="Relax and enjoy the beach", location="Patong", day_id=day_obj.id),
        ])

        if day == 2:
            db.add(Transfer(from_location="Phuket City", to_location="Patong Beach", mode="Car", day_id=day_obj.id))

    db.commit()

    # ----------------------
    # Krabi 5-Night Trip
    # ----------------------
    krabi_trip = Itinerary(title="Krabi Explorer", duration=5, region="Krabi")
    db.add(krabi_trip)
    db.commit()

    for day in range(1, 6):
        day_obj = ItineraryDay(day_number=day, itinerary_id=krabi_trip.id)
        db.add(day_obj)
        db.commit()

        db.add_all([
            HotelAccommodation(name=f"Krabi Resort Day {day}", location="Ao Nang", day_id=day_obj.id),
            Activity(name=f"Island Hopping Day {day}", description="Visit nearby islands", location="Railay", day_id=day_obj.id),
        ])

        if day == 3:
            db.add(Transfer(from_location="Krabi Town", to_location="Railay", mode="Boat", day_id=day_obj.id))

    db.commit()

    # ----------------------
    # Recommended Itineraries
    # ----------------------
    rec1 = RecommendedItinerary(
        title="Phuket in 3 Nights",
        duration=3,
        region="Phuket",
        content=json.dumps({
            "days": [
                {"day": 1, "activities": ["Arrival", "Beach relaxation"]},
                {"day": 2, "activities": ["Phi Phi Island tour"]},
                {"day": 3, "activities": ["Local market shopping", "Departure"]}
            ]
        })
    )

    rec2 = RecommendedItinerary(
        title="Krabi Discovery in 5 Nights",
        duration=5,
        region="Krabi",
        content=json.dumps({
            "days": [
                {"day": 1, "activities": ["Check-in", "Sunset cruise"]},
                {"day": 2, "activities": ["Island hopping"]},
                {"day": 3, "activities": ["Visit Emerald Pool"]},
                {"day": 4, "activities": ["Free day"]},
                {"day": 5, "activities": ["Departure"]}
            ]
        })
    )

    db.add_all([rec1, rec2])
    db.commit()
    db.close()
    print("✅ Sample data seeded successfully.")

if __name__ == "__main__":
    seed_sample_data()

