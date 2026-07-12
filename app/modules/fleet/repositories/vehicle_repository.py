from sqlalchemy import select
from sqlalchemy.orm import Session
from app.modules.fleet.models.vehicle import Vehicle

class VehicleRepository:
    """
    Vehicle Repository Layer.
    Responsible exclusively for database queries and persistence.
    Contains no business validation, lifecycle checks, or formatting rules.
    """

    @staticmethod
    def create_vehicle(db: Session, vehicle: Vehicle) -> Vehicle:
        """
        Adds and persists a new vehicle to the database.
        """
        db.add(vehicle)
        db.commit()
        db.refresh(vehicle)
        return vehicle

    @staticmethod
    def update_vehicle(db: Session, vehicle: Vehicle) -> Vehicle:
        """
        Saves updates to an existing vehicle.
        """
        db.commit()
        db.refresh(vehicle)
        return vehicle

    @staticmethod
    def find_by_id(db: Session, vehicle_id: int) -> Vehicle | None:
        """
        Finds a vehicle by database primary key.
        """
        stmt = select(Vehicle).where(Vehicle.id == vehicle_id)
        return db.execute(stmt).scalar_one_or_none()

    @staticmethod
    def find_by_registration(db: Session, registration_number: str) -> Vehicle | None:
        """
        Finds a vehicle by exact registration number match.
        """
        stmt = select(Vehicle).where(Vehicle.registration_number == registration_number)
        return db.execute(stmt).scalar_one_or_none()

    @staticmethod
    def list_vehicles(db: Session) -> list[Vehicle]:
        """
        Lists all vehicles in the database.
        """
        stmt = select(Vehicle)
        return list(db.execute(stmt).scalars().all())
