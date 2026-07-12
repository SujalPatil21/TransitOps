from typing import Optional
from datetime import datetime
from decimal import Decimal
from pydantic import BaseModel, Field, field_validator
from app.modules.dispatcher.constants import TripStatus

class TripCreate(BaseModel):
    source: str = Field(..., description="Starting point of the trip")
    destination: str = Field(..., description="Ending point of the trip")
    cargo_weight_kg: float = Field(..., gt=0, description="Cargo weight must be greater than 0")
    planned_distance: float = Field(..., gt=0, description="Planned distance must be greater than 0")
    trip_revenue: Decimal = Field(..., ge=0, description="Trip revenue must be greater than or equal to 0")
    vehicle_id: int = Field(..., description="ID of the assigned vehicle")
    driver_id: int = Field(..., description="ID of the assigned driver")

    @field_validator('source', 'destination')
    @classmethod
    def trim_and_validate_non_empty(cls, v: str) -> str:
        trimmed = v.strip()
        if not trimmed:
            raise ValueError("Field must not be empty after trimming whitespace.")
        return trimmed

class TripUpdate(BaseModel):
    source: Optional[str] = Field(None, description="Starting point of the trip")
    destination: Optional[str] = Field(None, description="Ending point of the trip")
    cargo_weight_kg: Optional[float] = Field(None, gt=0, description="Cargo weight must be greater than 0")
    planned_distance: Optional[float] = Field(None, gt=0, description="Planned distance must be greater than 0")
    trip_revenue: Optional[Decimal] = Field(None, ge=0, description="Trip revenue must be greater than or equal to 0")
    vehicle_id: Optional[int] = Field(None, description="ID of the assigned vehicle")
    driver_id: Optional[int] = Field(None, description="ID of the assigned driver")

    @field_validator('source', 'destination')
    @classmethod
    def trim_and_validate_non_empty(cls, v: Optional[str]) -> Optional[str]:
        if v is None:
            return v
        trimmed = v.strip()
        if not trimmed:
            raise ValueError("Field must not be empty after trimming whitespace.")
        return trimmed

class TripComplete(BaseModel):
    # Empty schema since post-trip financial submission is deferred
    pass

class TripBaseResponse(BaseModel):
    id: int
    source: str
    destination: str
    cargo_weight_kg: float
    planned_distance: float
    trip_revenue: Decimal
    vehicle_id: int
    driver_id: int
    status: TripStatus
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
