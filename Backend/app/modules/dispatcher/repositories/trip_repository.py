from typing import Optional
from sqlalchemy import select
from sqlalchemy.orm import Session
from app.modules.dispatcher.models.trip import Trip
from app.modules.dispatcher.constants import TripStatus

class TripRepository:
    def create(self, db: Session, trip: Trip) -> Trip:
        """Creates a trip in draft state and commits immediately."""
        db.add(trip)
        db.commit()
        db.refresh(trip)
        return trip

    def get_by_id(self, db: Session, trip_id: int) -> Optional[Trip]:
        """Retrieves a trip by database primary key."""
        return db.query(Trip).filter(Trip.id == trip_id).first()

    def get_all(self, db: Session) -> list[Trip]:
        """Retrieves all trips in the database."""
        return db.query(Trip).all()

    def update(self, db: Session, trip: Trip) -> Trip:
        """Saves a draft trip updates and commits immediately."""
        db.commit()
        db.refresh(trip)
        return trip

    # Lifecycle-specific query infrastructure (non-committing)
    
    def get_by_id_for_update(self, db: Session, trip_id: int) -> Optional[Trip]:
        """Acquires a pessimistic write lock on a Trip row."""
        return db.query(Trip).with_for_update(of=Trip).filter(Trip.id == trip_id).first()

    def get_active_trip_for_vehicle(self, db: Session, vehicle_id: int, exclude_trip_id: Optional[int] = None) -> Optional[Trip]:
        """Checks if there is a conflicting DISPATCHED trip referencing the vehicle."""
        query = db.query(Trip).filter(
            Trip.vehicle_id == vehicle_id,
            Trip.status == TripStatus.DISPATCHED
        )
        if exclude_trip_id is not None:
            query = query.filter(Trip.id != exclude_trip_id)
        return query.first()

    def get_active_trip_for_driver(self, db: Session, driver_id: int, exclude_trip_id: Optional[int] = None) -> Optional[Trip]:
        """Checks if there is a conflicting DISPATCHED trip referencing the driver."""
        query = db.query(Trip).filter(
            Trip.driver_id == driver_id,
            Trip.status == TripStatus.DISPATCHED
        )
        if exclude_trip_id is not None:
            query = query.filter(Trip.id != exclude_trip_id)
        return query.first()
