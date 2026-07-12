from sqlalchemy.orm import Session
from app.modules.fleet.exceptions.vehicle_exception import DuplicateRegistrationException, VehicleValidationException

def validate_vehicle_data(capacity_kg: float, odometer: float) -> None:
    """
    Validates numeric values for capacity and odometer.
    """
    if capacity_kg <= 0:
        raise VehicleValidationException("Capacity must be a positive number.")
    if odometer < 0:
        raise VehicleValidationException("Odometer cannot be negative.")

def validate_registration_uniqueness(db: Session, registration_number: str, exclude_id: int = None) -> None:
    """
    Validates that the normalized registration number is unique.
    """
    from app.modules.fleet.repositories.vehicle_repository import VehicleRepository
    normalized = registration_number.strip().upper()
    existing = VehicleRepository.find_by_registration(db, normalized)
    if existing and (exclude_id is None or existing.id != exclude_id):
        raise DuplicateRegistrationException(normalized)
