import re
from sqlalchemy.orm import Session
from app.modules.safety.exceptions.driver_exception import (
    DuplicateEmployeeException,
    DuplicateEmailException,
    DuplicateLicenseException,
    DriverValidationException
)


def validate_email_format(email: str) -> None:
    """Validates email format using a standard regex pattern."""
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    if not re.match(pattern, email):
        raise DriverValidationException(f"Invalid email format: '{email}'.")


def validate_phone_format(phone: str) -> None:
    """Validates phone number format (digits, spaces, dashes, plus, parens; 7-20 chars)."""
    pattern = r'^[\d\s\-\+\(\)]{7,20}$'
    if not re.match(pattern, phone):
        raise DriverValidationException(f"Invalid phone number format: '{phone}'.")


def validate_driver_data(experience_years: int, safety_score: float) -> None:
    """Validates numeric ranges for experience and safety score."""
    if experience_years < 0:
        raise DriverValidationException("Experience years cannot be negative.")
    if safety_score < 0 or safety_score > 100:
        raise DriverValidationException("Safety score must be between 0 and 100.")


def validate_employee_uniqueness(db: Session, employee_id: str, exclude_id: int = None) -> None:
    """Validates that the normalized employee ID is unique."""
    from app.modules.safety.repositories.driver_repository import DriverRepository
    existing = DriverRepository.find_by_employee_id(db, employee_id)
    if existing and (exclude_id is None or existing.id != exclude_id):
        raise DuplicateEmployeeException(employee_id)


def validate_email_uniqueness(db: Session, email: str, exclude_id: int = None) -> None:
    """Validates that the email is unique."""
    from app.modules.safety.repositories.driver_repository import DriverRepository
    existing = DriverRepository.find_by_email(db, email)
    if existing and (exclude_id is None or existing.id != exclude_id):
        raise DuplicateEmailException(email)


def validate_license_uniqueness(db: Session, license_number: str, exclude_id: int = None) -> None:
    """Validates that the normalized license number is unique."""
    from app.modules.safety.repositories.driver_repository import DriverRepository
    existing = DriverRepository.find_by_license(db, license_number)
    if existing and (exclude_id is None or existing.id != exclude_id):
        raise DuplicateLicenseException(license_number)
