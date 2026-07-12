import datetime
from typing import List
from pydantic import BaseModel, ConfigDict

class VehicleResponse(BaseModel):
    """
    Response schema for a single vehicle.
    """
    id: int
    registration_number: str
    vehicle_type: str
    manufacturer: str
    model: str
    manufacturing_year: int
    capacity_kg: float
    odometer: float
    status: str
    created_at: datetime.datetime
    updated_at: datetime.datetime

    model_config = ConfigDict(from_attributes=True)

class VehicleListResponse(BaseModel):
    """
    Response schema for a list of vehicles.
    """
    vehicles: List[VehicleResponse]
