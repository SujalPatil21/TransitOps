import datetime
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from app.modules.safety.models.driver import Driver
from app.modules.safety.constants import DriverStatus
from app.modules.safety.exceptions.driver_exception import (
    DriverNotFoundException,
    DuplicateEmployeeException,
    DuplicateEmailException,
    DuplicateLicenseException,
    DriverValidationException,
    DriverSuspensionException
)
from app.modules.safety.repositories.driver_repository import DriverRepository
from app.modules.safety.validators.driver_validator import (
    validate_email_format,
    validate_phone_format,
    validate_driver_data,
    validate_employee_uniqueness,
    validate_email_uniqueness,
    validate_license_uniqueness
)
from app.modules.safety.schemas.request import DriverCreateRequest, DriverUpdateRequest


class DriverService:
    """
    Driver Service Layer.
    Orchestrates business processes, performs validation checks, enforces lifecycle
    status transitions, handles transactions, and standardizes data.
    """

    @staticmethod
    def create_driver(db: Session, req: DriverCreateRequest) -> Driver:
        """
        Creates and persists a new driver.
        Normalizes employee_id and license_number, validates all fields,
        checks uniqueness, and handles database IntegrityError.
        """
        normalized_emp = req.employee_id.strip().upper()
        normalized_lic = req.license_number.strip().upper()
        email_lower = req.email.strip().lower()

        # Business validations
        validate_email_format(email_lower)
        validate_phone_format(req.phone)
        validate_driver_data(req.experience_years, req.safety_score)
        validate_employee_uniqueness(db, normalized_emp)
        validate_email_uniqueness(db, email_lower)
        validate_license_uniqueness(db, normalized_lic)

        driver = Driver(
            employee_id=normalized_emp,
            full_name=req.full_name.strip(),
            email=email_lower,
            phone=req.phone.strip(),
            license_number=normalized_lic,
            license_category=req.license_category.strip(),
            license_expiry=req.license_expiry,
            experience_years=req.experience_years,
            safety_score=req.safety_score,
            status=DriverStatus.AVAILABLE.value
        )

        try:
            return DriverRepository.create_driver(db, driver)
        except IntegrityError:
            db.rollback()
            # Determine which unique constraint was violated
            raise DuplicateEmployeeException(normalized_emp)
        except Exception:
            db.rollback()
            raise

    @staticmethod
    def get_driver_by_id(db: Session, driver_id: int) -> Driver:
        """Retrieves a driver by database primary key. Raises DriverNotFoundException if not found."""
        driver = DriverRepository.find_by_id(db, driver_id)
        if not driver:
            raise DriverNotFoundException()
        return driver

    @staticmethod
    def list_drivers(db: Session) -> list[Driver]:
        """Returns all registered drivers."""
        return DriverRepository.list_drivers(db)

    @staticmethod
    def search_drivers(db: Session, query: str = None, status_filter: str = None) -> list[Driver]:
        """Searches drivers by name, employee_id, or license_number."""
        return DriverRepository.search_drivers(db, query, status_filter)

    @staticmethod
    def update_driver(db: Session, driver_id: int, req: DriverUpdateRequest) -> Driver:
        """
        Partially updates an existing driver's information.
        Omitted fields remain unchanged. Direct status modification is rejected.
        Updates to SUSPENDED drivers are blocked.
        """
        driver = DriverRepository.find_by_id(db, driver_id)
        if not driver:
            raise DriverNotFoundException()

        # Block updates to suspended drivers
        if driver.status == DriverStatus.SUSPENDED.value:
            raise DriverValidationException("Cannot update a suspended driver. Reactivate first.")

        # Extract only explicitly provided fields
        update_data = req.model_dump(exclude_unset=True)

        # Safety check: Reject direct status updates
        if "status" in update_data:
            raise DriverValidationException("Driver status is controlled by business workflows and cannot be modified directly.")

        # If email is updated, validate and check uniqueness
        if "email" in update_data and update_data["email"]:
            email_lower = update_data["email"].strip().lower()
            update_data["email"] = email_lower
            validate_email_format(email_lower)
            validate_email_uniqueness(db, email_lower, exclude_id=driver_id)

        # If phone is updated, validate format
        if "phone" in update_data and update_data["phone"]:
            validate_phone_format(update_data["phone"].strip())
            update_data["phone"] = update_data["phone"].strip()

        # If license_number is updated, normalize and check uniqueness
        if "license_number" in update_data and update_data["license_number"]:
            normalized_lic = update_data["license_number"].strip().upper()
            update_data["license_number"] = normalized_lic
            validate_license_uniqueness(db, normalized_lic, exclude_id=driver_id)

        # Validate numeric ranges
        target_exp = update_data.get("experience_years", driver.experience_years)
        target_score = update_data.get("safety_score", driver.safety_score)
        validate_driver_data(target_exp, target_score)

        # Apply modifications
        for key, value in update_data.items():
            setattr(driver, key, value)

        driver.updated_at = datetime.datetime.now(datetime.timezone.utc)

        try:
            return DriverRepository.update_driver(db, driver)
        except IntegrityError:
            db.rollback()
            raise DuplicateEmployeeException(driver.employee_id)
        except Exception:
            db.rollback()
            raise

    @staticmethod
    def suspend_driver(db: Session, driver_id: int) -> Driver:
        """
        Suspends a driver. Only AVAILABLE drivers can be suspended.
        """
        driver = DriverRepository.find_by_id(db, driver_id)
        if not driver:
            raise DriverNotFoundException()

        if driver.status != DriverStatus.AVAILABLE.value:
            raise DriverSuspensionException(
                f"Driver cannot be suspended. Current status is '{driver.status}', but it must be 'AVAILABLE'."
            )

        driver.status = DriverStatus.SUSPENDED.value
        driver.updated_at = datetime.datetime.now(datetime.timezone.utc)

        try:
            return DriverRepository.update_driver(db, driver)
        except Exception:
            db.rollback()
            raise

    @staticmethod
    def activate_driver(db: Session, driver_id: int) -> Driver:
        """
        Reactivates a suspended driver. Only SUSPENDED drivers can be activated.
        """
        driver = DriverRepository.find_by_id(db, driver_id)
        if not driver:
            raise DriverNotFoundException()

        if driver.status != DriverStatus.SUSPENDED.value:
            raise DriverSuspensionException(
                f"Driver cannot be activated. Current status is '{driver.status}', but it must be 'SUSPENDED'."
            )

        driver.status = DriverStatus.AVAILABLE.value
        driver.updated_at = datetime.datetime.now(datetime.timezone.utc)

        try:
            return DriverRepository.update_driver(db, driver)
        except Exception:
            db.rollback()
            raise

    @staticmethod
    def get_expired_drivers(db: Session) -> list[Driver]:
        """Returns drivers with expired licenses."""
        return DriverRepository.find_expired_licenses(db)

    @staticmethod
    def get_expiring_soon_drivers(db: Session, days: int = 30) -> list[Driver]:
        """Returns drivers whose licenses expire within the given number of days."""
        return DriverRepository.find_expiring_soon(db, days)

    @staticmethod
    def get_dashboard(db: Session) -> dict:
        """Returns dashboard statistics for the Safety module."""
        return {
            "total_drivers": DriverRepository.count_total(db),
            "available": DriverRepository.count_by_status(db, DriverStatus.AVAILABLE.value),
            "on_trip": DriverRepository.count_by_status(db, DriverStatus.ON_TRIP.value),
            "off_duty": DriverRepository.count_by_status(db, DriverStatus.OFF_DUTY.value),
            "suspended": DriverRepository.count_by_status(db, DriverStatus.SUSPENDED.value),
            "expired_licenses": DriverRepository.count_expired_licenses(db),
            "expiring_soon": DriverRepository.count_expiring_soon(db)
        }
