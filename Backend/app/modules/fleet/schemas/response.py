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

class VehicleFrontendResponse(BaseModel):
    """
    Response schema mapped to frontend camelCase expectations.
    """
    id: int
    regNo: str
    model: str
    type: str
    capacity: float
    odometer: float
    cost: float = 0.0  # Optional/dummy field to satisfy frontend mock
    status: str

    @classmethod
    def from_orm(cls, vehicle):
        return cls(
            id=vehicle.id,
            regNo=vehicle.registration_number,
            model=vehicle.model,
            type=vehicle.vehicle_type,
            capacity=vehicle.capacity_kg,
            odometer=vehicle.odometer,
            status=vehicle.status
        )

class MaintenanceFrontendResponse(BaseModel):
    """
    Response schema mapped to frontend expectations for Maintenance logs.
    """
    id: int
    vehicleRegNo: str
    vehicleModel: str
    description: str
    startDate: str
    endDate: str
    cost: float
    status: str

    @classmethod
    def from_orm_joined(cls, maintenance, vehicle):
        return cls(
            id=maintenance.id,
            vehicleRegNo=vehicle.registration_number,
            vehicleModel=vehicle.model,
            description=maintenance.description,
            startDate=maintenance.start_date.strftime("%Y-%m-%d"),
            endDate=maintenance.end_date.strftime("%Y-%m-%d") if maintenance.end_date else "—",
            cost=maintenance.cost,
            status=maintenance.status
        )
