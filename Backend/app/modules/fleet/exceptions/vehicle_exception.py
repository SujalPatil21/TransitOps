from app.auth.exceptions.exceptions import AuthException
from fastapi import status

# TODO:
# FleetException currently inherits from AuthException only to reuse the existing global exception handler.
# During post-hackathon refactoring this should inherit from a shared application exception instead.
class FleetException(AuthException):
    """
    Base Exception class for Fleet related errors.
    Inherits from AuthException to utilize the existing global exception handler.
    """
    def __init__(self, message: str, error_code: str, status_code: int = status.HTTP_400_BAD_REQUEST, data: dict = None):
        super().__init__(
            message=message,
            error_code=error_code,
            status_code=status_code,
            data=data
        )

class VehicleNotFoundException(FleetException):
    def __init__(self, message: str = "Vehicle not found."):
        super().__init__(
            message=message,
            error_code="VEHICLE_NOT_FOUND",
            status_code=status.HTTP_404_NOT_FOUND
        )

class DuplicateRegistrationException(FleetException):
    def __init__(self, registration_number: str):
        super().__init__(
            message=f"Vehicle with registration number '{registration_number}' already exists.",
            error_code="DUPLICATE_REGISTRATION",
            status_code=status.HTTP_409_CONFLICT
        )

class VehicleRetirementException(FleetException):
    def __init__(self, message: str):
        super().__init__(
            message=message,
            error_code="VEHICLE_RETIREMENT_FAILED",
            status_code=status.HTTP_400_BAD_REQUEST
        )

class VehicleValidationException(FleetException):
    def __init__(self, message: str, error_code: str = "VEHICLE_VALIDATION_FAILED"):
        super().__init__(
            message=message,
            error_code=error_code,
            status_code=status.HTTP_400_BAD_REQUEST
        )
