from sqlalchemy.orm import Session
from app.modules.dispatcher.models.trip import Trip

class TripRepository:
    def create(self, db: Session, trip: Trip) -> Trip:
        db.add(trip)
        db.commit()
        db.refresh(trip)
        return trip

    def get_by_id(self, db: Session, trip_id: int) -> Trip:
        return db.query(Trip).filter(Trip.id == trip_id).first()

    def get_all(self, db: Session) -> list[Trip]:
        return db.query(Trip).all()

    def update(self, db: Session, trip: Trip) -> Trip:
        db.commit()
        db.refresh(trip)
        return trip
