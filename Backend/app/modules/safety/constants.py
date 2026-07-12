from enum import Enum

class DriverStatus(str, Enum):
    """
    DriverStatus enum defining the lifecycle status of a driver.

    NOTE: ON_TRIP and OFF_DUTY are owned by the Dispatcher module.
    Safety module only manages AVAILABLE <-> SUSPENDED transitions.
    """
    AVAILABLE = "AVAILABLE"
    ON_TRIP = "ON_TRIP"
    OFF_DUTY = "OFF_DUTY"
    SUSPENDED = "SUSPENDED"
