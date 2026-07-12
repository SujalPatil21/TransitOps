from fastapi import status
from app.auth.exceptions.exceptions import AuthException

class DispatcherException(AuthException):
    """Base exception for all Dispatcher-owned errors."""
    def __init__(self, message: str, error_code: str, status_code: int = status.HTTP_400_BAD_REQUEST):
        super().__init__(message=message, error_code=error_code, status_code=status_code)

class TripNotFoundException(DispatcherException):
    def __init__(self, message: str = "Trip not found."):
        super().__init__(message, "TRIP_NOT_FOUND", status.HTTP_404_NOT_FOUND)

class TripNotDraftException(DispatcherException):
    def __init__(self, message: str = "Only draft trips can be modified or dispatched."):
        super().__init__(message, "TRIP_NOT_DRAFT", status.HTTP_400_BAD_REQUEST)

class TripNotDispatchedException(DispatcherException):
    def __init__(self, message: str = "Only dispatched trips can be completed."):
        super().__init__(message, "TRIP_NOT_DISPATCHED", status.HTTP_400_BAD_REQUEST)

class VehicleNotFoundException(DispatcherException):
    def __init__(self, message: str = "Assigned vehicle not found."):
        super().__init__(message, "VEHICLE_NOT_FOUND", status.HTTP_404_NOT_FOUND)

class VehicleUnavailableException(DispatcherException):
    def __init__(self, message: str = "Vehicle is not available."):
        super().__init__(message, "VEHICLE_UNAVAILABLE", status.HTTP_409_CONFLICT)

class DriverNotFoundException(DispatcherException):
    def __init__(self, message: str = "Assigned driver not found."):
        super().__init__(message, "DRIVER_NOT_FOUND", status.HTTP_404_NOT_FOUND)

class DriverUnavailableException(DispatcherException):
    def __init__(self, message: str = "Driver is not available."):
        super().__init__(message, "DRIVER_UNAVAILABLE", status.HTTP_409_CONFLICT)

class DriverLicenseExpiredException(DispatcherException):
    def __init__(self, message: str = "Driver license is expired."):
        super().__init__(message, "LICENSE_EXPIRED", status.HTTP_400_BAD_REQUEST)

class VehicleCapacityExceededException(DispatcherException):
    def __init__(self, message: str = "Cargo weight exceeds vehicle capacity."):
        super().__init__(message, "CAPACITY_EXCEEDED", status.HTTP_400_BAD_REQUEST)

class ActiveTripConflictException(DispatcherException):
    def __init__(self, message: str = "Resource already has an active dispatched trip."):
        super().__init__(message, "ACTIVE_TRIP_CONFLICT", status.HTTP_409_CONFLICT)

class InconsistentCompletionStateException(DispatcherException):
    def __init__(self, message: str = "Trip completion state is inconsistent."):
        super().__init__(message, "INCONSISTENT_COMPLETION_STATE", status.HTTP_409_CONFLICT)

class InvalidTripInputException(DispatcherException):
    def __init__(self, message: str = "Invalid trip input data."):
        super().__init__(message, "INVALID_TRIP_INPUT", status.HTTP_400_BAD_REQUEST)
