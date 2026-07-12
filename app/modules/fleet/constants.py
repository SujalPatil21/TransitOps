from enum import Enum

class VehicleStatus(str, Enum):
    """
    VehicleStatus enum defining the lifecycle status of a vehicle.
    
    NOTE: This is a future shared enum. It will eventually be relocated
    to a shared place (e.g. app/common/constants.py or app/common/enums.py)
    when Dispatcher, Safety, and Analytics modules are integrated.
    """
    AVAILABLE = "AVAILABLE"
    ON_TRIP = "ON_TRIP"
    IN_SHOP = "IN_SHOP"
    RETIRED = "RETIRED"
