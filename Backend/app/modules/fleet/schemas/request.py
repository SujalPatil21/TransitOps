from typing import Any, Optional
from pydantic import BaseModel, Field, model_validator, field_validator

class VehicleCreateRequest(BaseModel):
    """
    Schema for creating a new vehicle.
    Blocks direct manual status assignment.
    """
    registration_number: str = Field(..., min_length=1, max_length=50)
    vehicle_type: str = Field(..., min_length=1, max_length=50)
    manufacturer: str = Field(..., min_length=1, max_length=100)
    model: str = Field(..., min_length=1, max_length=100)
    manufacturing_year: int = Field(...)
    capacity_kg: float = Field(...)
    odometer: float = Field(...)

    @model_validator(mode="before")
    @classmethod
    def check_status_not_present(cls, data: Any) -> Any:
        if isinstance(data, dict) and "status" in data:
            raise ValueError("Vehicle status is controlled by business workflows and cannot be modified directly.")
        return data

    @field_validator("capacity_kg")
    @classmethod
    def validate_capacity(cls, v: float) -> float:
        if v <= 0:
            raise ValueError("Capacity must be a positive number.")
        return v

    @field_validator("odometer")
    @classmethod
    def validate_odometer(cls, v: float) -> float:
        if v < 0:
            raise ValueError("Odometer cannot be negative.")
        return v

class VehicleUpdateRequest(BaseModel):
    """
    Schema for updating an existing vehicle's information.
    Blocks direct manual status updates.
    """
    registration_number: Optional[str] = Field(None, min_length=1, max_length=50)
    vehicle_type: Optional[str] = Field(None, min_length=1, max_length=50)
    manufacturer: Optional[str] = Field(None, min_length=1, max_length=100)
    model: Optional[str] = Field(None, min_length=1, max_length=100)
    manufacturing_year: Optional[int] = Field(None)
    capacity_kg: Optional[float] = Field(None)
    odometer: Optional[float] = Field(None)

    @model_validator(mode="before")
    @classmethod
    def check_status_not_present(cls, data: Any) -> Any:
        if isinstance(data, dict) and "status" in data:
            raise ValueError("Vehicle status is controlled by business workflows and cannot be modified directly.")
        return data

    @field_validator("capacity_kg")
    @classmethod
    def validate_capacity(cls, v: Optional[float]) -> Optional[float]:
        if v is not None and v <= 0:
            raise ValueError("Capacity must be a positive number.")
        return v

    @field_validator("odometer")
    @classmethod
    def validate_odometer(cls, v: Optional[float]) -> Optional[float]:
        if v is not None and v < 0:
            raise ValueError("Odometer cannot be negative.")
        return v

class MaintenanceCreateRequest(BaseModel):
    """
    Schema for creating a new maintenance record.
    """
    vehicle_id: int = Field(...)
    description: str = Field(..., min_length=1, max_length=255)
    cost: float = Field(...)

    @field_validator("cost")
    @classmethod
    def validate_cost(cls, v: float) -> float:
        if v < 0:
            raise ValueError("Cost cannot be negative.")
        return v
