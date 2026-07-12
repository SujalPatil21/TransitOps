import datetime
from decimal import Decimal
from typing import Optional
from sqlalchemy.orm import Session
from sqlalchemy import select

from app.modules.dispatcher.models.trip import Trip
from app.modules.dispatcher.schemas.trip import TripCreate, TripUpdate, TripComplete
from app.modules.dispatcher.repositories.trip_repository import TripRepository
from app.modules.dispatcher.constants import TripStatus
from app.modules.dispatcher.exceptions.exceptions import (
    TripNotFoundException,
    TripNotDraftException,
    TripNotDispatchedException,
    VehicleNotFoundException,
    VehicleUnavailableException,
    DriverNotFoundException,
    DriverUnavailableException,
    DriverLicenseExpiredException,
    VehicleCapacityExceededException,
    ActiveTripConflictException,
    InconsistentCompletionStateException,
    InvalidTripInputException
)
from app.modules.fleet.models.vehicle import Vehicle
from app.modules.fleet.constants import VehicleStatus
from app.modules.safety.models.driver import Driver
from app.modules.safety.constants import DriverStatus

class TripService:
    def __init__(self, repository: TripRepository):
        self.repository = repository

    def _get_trip_or_404(self, db: Session, trip_id: int) -> Trip:
        trip = self.repository.get_by_id(db, trip_id)
        if not trip:
            raise TripNotFoundException()
        return trip

    def create_trip(self, db: Session, data: TripCreate) -> Trip:
        # Validate Vehicle exists
        vehicle = db.query(Vehicle).filter(Vehicle.id == data.vehicle_id).first()
        if not vehicle:
            raise VehicleNotFoundException()

        # Validate Driver exists
        driver = db.query(Driver).filter(Driver.id == data.driver_id).first()
        if not driver:
            raise DriverNotFoundException()

        trip = Trip(
            source=data.source.strip(),
            destination=data.destination.strip(),
            cargo_weight_kg=data.cargo_weight_kg,
            planned_distance=data.planned_distance,
            trip_revenue=data.trip_revenue,
            vehicle_id=data.vehicle_id,
            driver_id=data.driver_id,
            status=TripStatus.DRAFT
        )
        return self.repository.create(db, trip)

    def get_trip(self, db: Session, trip_id: int) -> Trip:
        return self._get_trip_or_404(db, trip_id)

    def list_trips(self, db: Session) -> list[Trip]:
        return self.repository.get_all(db)

    def update_draft(self, db: Session, trip_id: int, data: TripUpdate) -> Trip:
        try:
            # 1. Lock Trip Row first (prevent Draft update vs Dispatch race)
            trip = self.repository.get_by_id_for_update(db, trip_id)
            if not trip:
                raise TripNotFoundException()
            
            # 2. Check status after lock
            if trip.status != TripStatus.DRAFT:
                raise TripNotDraftException()

            if data.vehicle_id is not None:
                vehicle = db.query(Vehicle).filter(Vehicle.id == data.vehicle_id).first()
                if not vehicle:
                    raise VehicleNotFoundException()
                trip.vehicle_id = data.vehicle_id

            if data.driver_id is not None:
                driver = db.query(Driver).filter(Driver.id == data.driver_id).first()
                if not driver:
                    raise DriverNotFoundException()
                trip.driver_id = data.driver_id

            if data.source is not None:
                trip.source = data.source.strip()
            if data.destination is not None:
                trip.destination = data.destination.strip()
            if data.cargo_weight_kg is not None:
                trip.cargo_weight_kg = data.cargo_weight_kg
            if data.planned_distance is not None:
                trip.planned_distance = data.planned_distance
            if data.trip_revenue is not None:
                trip.trip_revenue = data.trip_revenue

            db.commit()
        except Exception:
            db.rollback()
            raise
        db.refresh(trip)
        return trip

    def dispatch_trip(self, db: Session, trip_id: int) -> Trip:
        try:
            # 1. Lock Trip Row
            trip = self.repository.get_by_id_for_update(db, trip_id)
            if not trip:
                raise TripNotFoundException()

            if trip.status != TripStatus.DRAFT:
                raise TripNotDraftException()

            if not trip.vehicle_id:
                raise InvalidTripInputException("Trip does not have an assigned vehicle.")
            if not trip.driver_id:
                raise InvalidTripInputException("Trip does not have an assigned driver.")

            # 2. Lock Vehicle Row
            vehicle = db.query(Vehicle).with_for_update(of=Vehicle).filter(Vehicle.id == trip.vehicle_id).first()
            if not vehicle:
                raise VehicleNotFoundException()

            # 3. Lock Driver Row
            driver = db.query(Driver).with_for_update(of=Driver).filter(Driver.id == trip.driver_id).first()
            if not driver:
                raise DriverNotFoundException()

            # 4. Revalidate all business rules after locks are acquired
            if vehicle.status != VehicleStatus.AVAILABLE.value:
                raise VehicleUnavailableException()

            if driver.status != DriverStatus.AVAILABLE.value:
                raise DriverUnavailableException()

            # License expiry date check (License remains valid throughout expiry date)
            now_date = datetime.datetime.now(datetime.timezone.utc).date()
            expiry = driver.license_expiry
            if expiry.tzinfo is None:
                now_date = datetime.datetime.now().date()
            if expiry.date() < now_date:
                raise DriverLicenseExpiredException()

            # Exclusivity check - verify no other active trip references vehicle
            conflict_vehicle = self.repository.get_active_trip_for_vehicle(db, vehicle.id, exclude_trip_id=trip.id)
            if conflict_vehicle:
                raise ActiveTripConflictException("Vehicle is assigned to another active dispatched trip.")

            # Exclusivity check - verify no other active trip references driver
            conflict_driver = self.repository.get_active_trip_for_driver(db, driver.id, exclude_trip_id=trip.id)
            if conflict_driver:
                raise ActiveTripConflictException("Driver is assigned to another active dispatched trip.")

            # Capacity check
            if trip.cargo_weight_kg > vehicle.capacity_kg:
                raise VehicleCapacityExceededException()

            # 5. Mutate managed ORM entities
            trip.status = TripStatus.DISPATCHED
            vehicle.status = VehicleStatus.ON_TRIP.value
            driver.status = DriverStatus.ON_TRIP.value

            db.commit()
        except Exception:
            db.rollback()
            raise
        db.refresh(trip)
        return trip

    def complete_trip(self, db: Session, trip_id: int) -> Trip:
        try:
            # 1. Lock Trip Row
            trip = self.repository.get_by_id_for_update(db, trip_id)
            if not trip:
                raise TripNotFoundException()

            if trip.status != TripStatus.DISPATCHED:
                raise TripNotDispatchedException()

            if not trip.vehicle_id or not trip.driver_id:
                raise InconsistentCompletionStateException("Trip missing resource assignments.")

            # 2. Lock Vehicle Row
            vehicle = db.query(Vehicle).with_for_update(of=Vehicle).filter(Vehicle.id == trip.vehicle_id).first()
            if not vehicle:
                raise VehicleNotFoundException()

            # 3. Lock Driver Row
            driver = db.query(Driver).with_for_update(of=Driver).filter(Driver.id == trip.driver_id).first()
            if not driver:
                raise DriverNotFoundException()

            # 4. Revalidate all business rules after locks are acquired
            if vehicle.status != VehicleStatus.ON_TRIP.value:
                raise InconsistentCompletionStateException("Vehicle is not currently on a trip.")

            if driver.status != DriverStatus.ON_TRIP.value:
                raise InconsistentCompletionStateException("Driver is not currently on a trip.")

            if vehicle.id != trip.vehicle_id:
                raise InconsistentCompletionStateException("Locked vehicle ID does not match trip vehicle ID.")
            if driver.id != trip.driver_id:
                raise InconsistentCompletionStateException("Locked driver ID does not match trip driver ID.")

            # Verify no other active trip references them (excluding current)
            conflict_vehicle = self.repository.get_active_trip_for_vehicle(db, vehicle.id, exclude_trip_id=trip.id)
            if conflict_vehicle:
                raise ActiveTripConflictException("Vehicle is assigned to another active dispatched trip.")

            conflict_driver = self.repository.get_active_trip_for_driver(db, driver.id, exclude_trip_id=trip.id)
            if conflict_driver:
                raise ActiveTripConflictException("Driver is assigned to another active dispatched trip.")

            # 5. Mutate managed ORM entities (No post-trip financial updates)
            trip.status = TripStatus.COMPLETED
            vehicle.status = VehicleStatus.AVAILABLE.value
            driver.status = DriverStatus.AVAILABLE.value

            db.commit()
        except Exception:
            db.rollback()
            raise
        db.refresh(trip)
        return trip

    def list_eligible_vehicles(self, db: Session, cargo_weight_kg: Optional[float] = None) -> list[Vehicle]:
        dispatched_vehicle_ids = db.query(Trip.vehicle_id).filter(Trip.status == TripStatus.DISPATCHED).subquery()
        query = db.query(Vehicle).filter(
            Vehicle.status == VehicleStatus.AVAILABLE.value,
            ~Vehicle.id.in_(dispatched_vehicle_ids)
        )
        if cargo_weight_kg is not None:
            query = query.filter(Vehicle.capacity_kg >= cargo_weight_kg)
        return query.all()

    def list_eligible_drivers(self, db: Session) -> list[Driver]:
        dispatched_driver_ids = db.query(Trip.driver_id).filter(Trip.status == TripStatus.DISPATCHED).subquery()
        now_dt = datetime.datetime.now(datetime.timezone.utc)
        
        query = db.query(Driver).filter(
            Driver.status == DriverStatus.AVAILABLE.value,
            Driver.license_expiry >= now_dt,
            ~Driver.id.in_(dispatched_driver_ids)
        )
        return query.all()
