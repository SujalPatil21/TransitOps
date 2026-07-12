import datetime
from typing import List
from pydantic import BaseModel, ConfigDict


class DriverResponse(BaseModel):
    """Response schema for a single driver."""
    id: int
    employee_id: str
    full_name: str
    email: str
    phone: str
    license_number: str
    license_category: str
    license_expiry: datetime.datetime
    experience_years: int
    safety_score: float
    status: str
    created_at: datetime.datetime
    updated_at: datetime.datetime

    model_config = ConfigDict(from_attributes=True)


class DriverListResponse(BaseModel):
    """Response schema for a list of drivers."""
    drivers: List[DriverResponse]


class DashboardResponse(BaseModel):
    """Response schema for the Safety dashboard."""
    total_drivers: int
    available: int
    on_trip: int
    off_duty: int
    suspended: int
    expired_licenses: int
    expiring_soon: int
