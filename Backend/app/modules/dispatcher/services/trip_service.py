from sqlalchemy.orm import Session
from fastapi import status
from datetime import datetime
from app.modules.dispatcher.models.trip import Trip
from app.modules.dispatcher.schemas.trip import TripCreate, TripUpdate, TripComplete
from app.modules.dispatcher.repositories.trip_repository import TripRepository
from app.modules.dispatcher.exceptions.exceptions import DispatcherException
from app.modules.dispatcher.constants import TripStatus
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
            raise DispatcherException("Trip not found.", "TRIP_NOT_FOUND", status.HTTP_404_NOT_FOUND)
        return trip

    def create_trip(self, db: Session, data: TripCreate) -> Trip:
        trip = Trip(
            vehicle_id=data.vehicle_id,
            driver_id=data.driver_id,
            cargo_weight_kg=data.cargo_weight_kg,
            trip_revenue=data.trip_revenue,
            status=TripStatus.DRAFT
        )
        return self.repository.create(db, trip)

    def get_trip(self, db: Session, trip_id: int) -> Trip:
        return self._get_trip_or_404(db, trip_id)

    def list_trips(self, db: Session) -> list[Trip]:
        return self.repository.get_all(db)

    def update_draft(self, db: Session, trip_id: int, data: TripUpdate) -> Trip:
        trip = self._get_trip_or_404(db, trip_id)
        
        if trip.status != TripStatus.DRAFT:
            raise DispatcherException("Only draft trips can be updated.", "INVALID_TRIP_STATE")

        if data.vehicle_id is not None:
            trip.vehicle_id = data.vehicle_id
        if data.driver_id is not None:
            trip.driver_id = data.driver_id
        if data.cargo_weight_kg is not None:
            trip.cargo_weight_kg = data.cargo_weight_kg
        if data.trip_revenue is not None:
            trip.trip_revenue = data.trip_revenue

        return self.repository.update(db, trip)

    def dispatch_trip(self, db: Session, trip_id: int) -> Trip:
        trip = self._get_trip_or_404(db, trip_id)
        
        if trip.status != TripStatus.DRAFT:
            raise DispatcherException("Only draft trips can be dispatched.", "INVALID_TRIP_STATE")
            
        if not trip.vehicle_id:
            raise DispatcherException("Vehicle must be assigned to dispatch trip.", "MISSING_VEHICLE")
            
        if not trip.driver_id:
            raise DispatcherException("Driver must be assigned to dispatch trip.", "MISSING_DRIVER")

        # Validate Vehicle
        vehicle = db.query(Vehicle).filter(Vehicle.id == trip.vehicle_id).first()
        if not vehicle:
            raise DispatcherException("Assigned vehicle not found.", "VEHICLE_NOT_FOUND")
        if vehicle.status != VehicleStatus.AVAILABLE:
            raise DispatcherException("Vehicle is not available for dispatch.", "VEHICLE_UNAVAILABLE", status.HTTP_409_CONFLICT)
        if vehicle.capacity_kg < trip.cargo_weight_kg:
            raise DispatcherException("Cargo exceeds vehicle capacity.", "CAPACITY_EXCEEDED")

        # Validate Driver
        driver = db.query(Driver).filter(Driver.id == trip.driver_id).first()
        if not driver:
            raise DispatcherException("Assigned driver not found.", "DRIVER_NOT_FOUND")
        if driver.status != DriverStatus.AVAILABLE:
            raise DispatcherException("Driver is not available for dispatch.", "DRIVER_UNAVAILABLE", status.HTTP_409_CONFLICT)
        if driver.license_expiry < datetime.utcnow():
            raise DispatcherException("Driver license is expired.", "LICENSE_EXPIRED")

        # Atomic state updates
        trip.status = TripStatus.DISPATCHED
        vehicle.status = VehicleStatus.ON_TRIP
        driver.status = DriverStatus.ON_TRIP

        # We rely on flush/commit in update to save all
        return self.repository.update(db, trip)

    def complete_trip(self, db: Session, trip_id: int, data: TripComplete) -> Trip:
        trip = self._get_trip_or_404(db, trip_id)
        
        if trip.status != TripStatus.DISPATCHED:
            raise DispatcherException("Only dispatched trips can be completed.", "INVALID_TRIP_STATE")

        # Update operational data
        trip.fuel_consumed_l = data.fuel_consumed_l
        trip.fuel_cost = data.fuel_cost
        trip.toll_charges = data.toll_charges
        trip.other_expenses = data.other_expenses

        # Retrieve and release resources
        vehicle = db.query(Vehicle).filter(Vehicle.id == trip.vehicle_id).first()
        if vehicle:
            vehicle.status = VehicleStatus.AVAILABLE

        driver = db.query(Driver).filter(Driver.id == trip.driver_id).first()
        if driver:
            driver.status = DriverStatus.AVAILABLE

        trip.status = TripStatus.COMPLETED

        return self.repository.update(db, trip)
