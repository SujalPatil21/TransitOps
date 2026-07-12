import datetime
from typing import List
from pydantic import BaseModel, ConfigDict


class DriverFrontendResponse(BaseModel):
    """Response schema mapped to frontend camelCase expectations."""
    id: int
    name: str
    licenseNo: str
    category: str
    expiryDate: str
    contact: str
    safetyScore: float
    status: str
    
    # Adding for completeness based on DB model, though frontend may not show it yet
    empId: str
    tripCompletion: str = "N/A"
    
    @classmethod
    def from_orm(cls, driver):
        return cls(
            id=driver.id,
            name=driver.full_name,
            licenseNo=driver.license_number,
            category=driver.license_category,
            expiryDate=driver.license_expiry.strftime("%Y-%m-%d"),
            contact=driver.phone,
            safetyScore=driver.safety_score,
            status=driver.status,
            empId=driver.employee_id
        )


class DashboardResponse(BaseModel):
    """Response schema for the Safety dashboard."""
    total_drivers: int
    available: int
    on_trip: int
    off_duty: int
    suspended: int
    expired_licenses: int
    expiring_soon: int
