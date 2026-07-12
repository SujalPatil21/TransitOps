from typing import Any, Optional
from datetime import datetime
from pydantic import BaseModel, Field, model_validator, field_validator


class DriverCreateRequest(BaseModel):
    """Schema for creating a new driver. Blocks direct manual status assignment."""
    employee_id: str = Field(..., min_length=1, max_length=50)
    full_name: str = Field(..., min_length=1, max_length=150)
    email: str = Field(..., min_length=1, max_length=150)
    phone: str = Field(..., min_length=1, max_length=20)
    license_number: str = Field(..., min_length=1, max_length=50)
    license_category: str = Field(..., min_length=1, max_length=20)
    license_expiry: datetime = Field(...)
    experience_years: int = Field(..., ge=0)
    safety_score: float = Field(default=100.0, ge=0, le=100)

    @model_validator(mode="before")
    @classmethod
    def check_status_not_present(cls, data: Any) -> Any:
        if isinstance(data, dict) and "status" in data:
            raise ValueError("Driver status is controlled by business workflows and cannot be modified directly.")
        return data

    @field_validator("experience_years")
    @classmethod
    def validate_experience(cls, v: int) -> int:
        if v < 0:
            raise ValueError("Experience years cannot be negative.")
        return v

    @field_validator("safety_score")
    @classmethod
    def validate_safety_score(cls, v: float) -> float:
        if v < 0 or v > 100:
            raise ValueError("Safety score must be between 0 and 100.")
        return v


class DriverUpdateRequest(BaseModel):
    """Schema for partially updating a driver. Blocks direct manual status updates."""
    full_name: Optional[str] = Field(None, min_length=1, max_length=150)
    email: Optional[str] = Field(None, min_length=1, max_length=150)
    phone: Optional[str] = Field(None, min_length=1, max_length=20)
    license_number: Optional[str] = Field(None, min_length=1, max_length=50)
    license_category: Optional[str] = Field(None, min_length=1, max_length=20)
    license_expiry: Optional[datetime] = None
    experience_years: Optional[int] = Field(None, ge=0)
    safety_score: Optional[float] = Field(None, ge=0, le=100)

    @model_validator(mode="before")
    @classmethod
    def check_status_not_present(cls, data: Any) -> Any:
        if isinstance(data, dict) and "status" in data:
            raise ValueError("Driver status is controlled by business workflows and cannot be modified directly.")
        return data

    @field_validator("experience_years")
    @classmethod
    def validate_experience(cls, v: Optional[int]) -> Optional[int]:
        if v is not None and v < 0:
            raise ValueError("Experience years cannot be negative.")
        return v

    @field_validator("safety_score")
    @classmethod
    def validate_safety_score(cls, v: Optional[float]) -> Optional[float]:
        if v is not None and (v < 0 or v > 100):
            raise ValueError("Safety score must be between 0 and 100.")
        return v
