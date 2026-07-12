from typing import Optional
from datetime import datetime
from pydantic import BaseModel, Field
from app.modules.dispatcher.constants import TripStatus

class TripCreate(BaseModel):
    vehicle_id: Optional[int] = None
    driver_id: Optional[int] = None
    cargo_weight_kg: float = Field(..., gt=0, description="Cargo weight must be greater than 0")
    trip_revenue: Optional[float] = Field(None, ge=0)

class TripUpdate(BaseModel):
    vehicle_id: Optional[int] = None
    driver_id: Optional[int] = None
    cargo_weight_kg: Optional[float] = Field(None, gt=0)
    trip_revenue: Optional[float] = Field(None, ge=0)

class TripComplete(BaseModel):
    fuel_consumed_l: float = Field(..., ge=0)
    fuel_cost: float = Field(..., ge=0)
    toll_charges: float = Field(..., ge=0)
    other_expenses: float = Field(..., ge=0)

class TripBaseResponse(BaseModel):
    id: int
    vehicle_id: Optional[int]
    driver_id: Optional[int]
    status: TripStatus
    cargo_weight_kg: float
    trip_revenue: Optional[float]
    fuel_consumed_l: Optional[float]
    fuel_cost: Optional[float]
    toll_charges: Optional[float]
    other_expenses: Optional[float]
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
