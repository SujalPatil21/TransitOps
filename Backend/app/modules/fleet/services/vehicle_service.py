import datetime
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from app.modules.fleet.models.vehicle import Vehicle
from app.modules.fleet.constants import VehicleStatus
from app.modules.fleet.exceptions.vehicle_exception import (
    VehicleNotFoundException,
    DuplicateRegistrationException,
    VehicleRetirementException,
    VehicleValidationException
)
from app.modules.fleet.repositories.vehicle_repository import VehicleRepository
from app.modules.fleet.validators.vehicle_validator import validate_vehicle_data, validate_registration_uniqueness
from app.modules.fleet.schemas.request import VehicleCreateRequest, VehicleUpdateRequest

class VehicleService:
    """
    Vehicle Service Layer.
    Orchestrates business processes, performs validation checks, enforces lifecycle 
    status transitions, handles transactions, and standardizes data.
    """

    @staticmethod
    def create_vehicle(db: Session, req: VehicleCreateRequest) -> Vehicle:
        """
        Creates and persists a new vehicle.
        Normalizes the registration number, validates capacity & odometer,
        checks uniqueness, and handles database IntegrityError.
        """
        normalized_reg = req.registration_number.strip().upper()

        # Perform business validations
        validate_vehicle_data(req.capacity_kg, req.odometer)
        validate_registration_uniqueness(db, normalized_reg)

        vehicle = Vehicle(
            registration_number=normalized_reg,
            vehicle_type=req.vehicle_type,
            manufacturer=req.manufacturer,
            model=req.model,
            manufacturing_year=req.manufacturing_year,
            capacity_kg=req.capacity_kg,
            odometer=req.odometer,
            status=VehicleStatus.AVAILABLE.value
        )

        try:
            return VehicleRepository.create_vehicle(db, vehicle)
        except IntegrityError:
            db.rollback()
            raise DuplicateRegistrationException(normalized_reg)
        except Exception:
            db.rollback()
            raise

    @staticmethod
    def get_vehicle_by_id(db: Session, vehicle_id: int) -> Vehicle:
        """
        Retrieves a vehicle by database primary key.
        Raises VehicleNotFoundException if it does not exist.
        """
        vehicle = VehicleRepository.find_by_id(db, vehicle_id)
        if not vehicle:
            raise VehicleNotFoundException()
        return vehicle

    @staticmethod
    def list_vehicles(db: Session) -> list[Vehicle]:
        """
        Returns all registered vehicles.
        """
        return VehicleRepository.list_vehicles(db)

    @staticmethod
    def update_vehicle(db: Session, vehicle_id: int, req: VehicleUpdateRequest) -> Vehicle:
        """
        Partially updates an existing vehicle's information.
        Omitted fields remain unchanged. Direct status modification is rejected.
        Updates to already retired vehicles are blocked.
        """
        vehicle = VehicleRepository.find_by_id(db, vehicle_id)
        if not vehicle:
            raise VehicleNotFoundException()

        # Block updates to retired vehicles
        if vehicle.status == VehicleStatus.RETIRED.value:
            raise VehicleValidationException("Cannot update a retired vehicle.")

        # Extract only explicitly provided fields
        update_data = req.model_dump(exclude_unset=True)

        # Safety check: Reject direct status updates (blocked in schema, but checked here as well)
        if "status" in update_data:
            raise VehicleValidationException("Vehicle status is controlled by business workflows and cannot be modified directly.")

        # If registration number is updated, normalize and assert uniqueness
        if "registration_number" in update_data and update_data["registration_number"]:
            normalized_reg = update_data["registration_number"].strip().upper()
            update_data["registration_number"] = normalized_reg
            validate_registration_uniqueness(db, normalized_reg, exclude_id=vehicle_id)

        # Validate numeric ranges
        target_capacity = update_data.get("capacity_kg", vehicle.capacity_kg)
        target_odometer = update_data.get("odometer", vehicle.odometer)
        validate_vehicle_data(target_capacity, target_odometer)

        # Apply modifications
        for key, value in update_data.items():
            setattr(vehicle, key, value)

        vehicle.updated_at = datetime.datetime.now(datetime.timezone.utc)

        try:
            return VehicleRepository.update_vehicle(db, vehicle)
        except IntegrityError:
            db.rollback()
            reg_num = update_data.get("registration_number", vehicle.registration_number)
            raise DuplicateRegistrationException(reg_num)
        except Exception:
            db.rollback()
            raise

    @staticmethod
    def retire_vehicle(db: Session, vehicle_id: int) -> Vehicle:
        """
        Retires a vehicle. Retirement is irreversible.
        A vehicle can only be retired if its status is AVAILABLE.
        Rejects retirement if vehicle is ON_TRIP, IN_SHOP, or already RETIRED.
        """
        vehicle = VehicleRepository.find_by_id(db, vehicle_id)
        if not vehicle:
            raise VehicleNotFoundException()

        # Enforcement of retirement transition rule
        if vehicle.status != VehicleStatus.AVAILABLE.value:
            raise VehicleRetirementException(
                f"Vehicle cannot be retired. Current status is '{vehicle.status}', but it must be 'AVAILABLE'."
            )

        vehicle.status = VehicleStatus.RETIRED.value
        vehicle.updated_at = datetime.datetime.now(datetime.timezone.utc)

        try:
            return VehicleRepository.update_vehicle(db, vehicle)
        except Exception:
            db.rollback()
            raise
