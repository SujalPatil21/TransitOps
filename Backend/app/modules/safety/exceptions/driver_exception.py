from app.auth.exceptions.exceptions import AuthException
from fastapi import status


class SafetyException(AuthException):
    """
    Base Exception class for Safety related errors.
    Inherits from AuthException to utilize the existing global exception handler.
    """
    def __init__(self, message: str, error_code: str, status_code: int = status.HTTP_400_BAD_REQUEST, data: dict = None):
        super().__init__(
            message=message,
            error_code=error_code,
            status_code=status_code,
            data=data
        )


class DriverNotFoundException(SafetyException):
    def __init__(self, message: str = "Driver not found."):
        super().__init__(
            message=message,
            error_code="DRIVER_NOT_FOUND",
            status_code=status.HTTP_404_NOT_FOUND
        )


class DuplicateEmployeeException(SafetyException):
    def __init__(self, employee_id: str):
        super().__init__(
            message=f"Driver with employee ID '{employee_id}' already exists.",
            error_code="DUPLICATE_EMPLOYEE_ID",
            status_code=status.HTTP_409_CONFLICT
        )


class DuplicateEmailException(SafetyException):
    def __init__(self, email: str):
        super().__init__(
            message=f"Driver with email '{email}' already exists.",
            error_code="DUPLICATE_EMAIL",
            status_code=status.HTTP_409_CONFLICT
        )


class DuplicateLicenseException(SafetyException):
    def __init__(self, license_number: str):
        super().__init__(
            message=f"Driver with license number '{license_number}' already exists.",
            error_code="DUPLICATE_LICENSE",
            status_code=status.HTTP_409_CONFLICT
        )


class DriverValidationException(SafetyException):
    def __init__(self, message: str, error_code: str = "DRIVER_VALIDATION_FAILED"):
        super().__init__(
            message=message,
            error_code=error_code,
            status_code=status.HTTP_400_BAD_REQUEST
        )


class DriverSuspensionException(SafetyException):
    def __init__(self, message: str):
        super().__init__(
            message=message,
            error_code="DRIVER_SUSPENSION_FAILED",
            status_code=status.HTTP_400_BAD_REQUEST
        )


class LicenseExpiredException(SafetyException):
    def __init__(self, message: str = "Driver license has expired."):
        super().__init__(
            message=message,
            error_code="LICENSE_EXPIRED",
            status_code=status.HTTP_400_BAD_REQUEST
        )
