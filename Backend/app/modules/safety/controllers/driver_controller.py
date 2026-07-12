from typing import Optional
from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.orm import Session
from app.database.database import get_db
from app.auth.constants import UserRole
from app.auth.security.permissions import require_roles
from app.common.responses import APIResponse
from app.modules.safety.schemas.request import DriverCreateRequest, DriverUpdateRequest
from app.modules.safety.schemas.response import DriverFrontendResponse, DashboardResponse
from app.modules.safety.services.driver_service import DriverService

# Set up the Safety module router with role-based restriction
router = APIRouter(
    prefix="/safety",
    tags=["Safety"],
    dependencies=[Depends(require_roles(UserRole.SAFETY_OFFICER))]
)

@router.get("/dashboard", status_code=status.HTTP_200_OK)
def get_dashboard(db: Session = Depends(get_db)):
    """HTTP GET: Returns Safety dashboard statistics."""
    dashboard = DriverService.get_dashboard(db)
    data = DashboardResponse(**dashboard).model_dump(mode="json")
    return APIResponse.success(
        message="Dashboard retrieved successfully.",
        data={"dashboard": data},
        status_code=status.HTTP_200_OK
    )

@router.get("/drivers/expired", status_code=status.HTTP_200_OK)
def get_expired_drivers(db: Session = Depends(get_db)):
    """HTTP GET: Returns drivers with expired licenses."""
    drivers = DriverService.get_expired_drivers(db)
    data = [DriverFrontendResponse.from_orm(d).model_dump(mode="json") for d in drivers]
    return APIResponse.success(
        message="Expired license drivers retrieved successfully.",
        data={"drivers": data},
        status_code=status.HTTP_200_OK
    )

@router.get("/drivers/expiring", status_code=status.HTTP_200_OK)
def get_expiring_drivers(days: int = Query(default=30, ge=1), db: Session = Depends(get_db)):
    """HTTP GET: Returns drivers whose licenses expire within the given number of days."""
    drivers = DriverService.get_expiring_soon_drivers(db, days)
    data = [DriverFrontendResponse.from_orm(d).model_dump(mode="json") for d in drivers]
    return APIResponse.success(
        message="Expiring license drivers retrieved successfully.",
        data={"drivers": data},
        status_code=status.HTTP_200_OK
    )

@router.get("/drivers/{id}", status_code=status.HTTP_200_OK)
def get_driver(id: int, db: Session = Depends(get_db)):
    """HTTP GET: Retrieves details for a specific driver by database ID."""
    driver = DriverService.get_driver_by_id(db, id)
    data = DriverFrontendResponse.from_orm(driver).model_dump(mode="json")
    return APIResponse.success(
        message="Driver details retrieved successfully.",
        data={"driver": data},
        status_code=status.HTTP_200_OK
    )

@router.get("/drivers", status_code=status.HTTP_200_OK)
def list_drivers(
    search: Optional[str] = Query(None),
    status_filter: Optional[str] = Query(None, alias="status"),
    db: Session = Depends(get_db)
):
    """HTTP GET: Retrieves a list of all registered drivers with optional search/filter."""
    if search or status_filter:
        drivers = DriverService.search_drivers(db, search, status_filter)
    else:
        drivers = DriverService.list_drivers(db)
    data = [DriverFrontendResponse.from_orm(d).model_dump(mode="json") for d in drivers]
    return APIResponse.success(
        message="Driver registry retrieved successfully.",
        data={"drivers": data},
        status_code=status.HTTP_200_OK
    )

@router.post("/drivers", status_code=status.HTTP_201_CREATED)
def create_driver(req: DriverCreateRequest, db: Session = Depends(get_db)):
    """HTTP POST: Registers a new driver in the system."""
    driver = DriverService.create_driver(db, req)
    data = DriverFrontendResponse.from_orm(driver).model_dump(mode="json")
    return APIResponse.success(
        message="Driver registered successfully.",
        data={"driver": data},
        status_code=status.HTTP_201_CREATED
    )

@router.patch("/drivers/{id}", status_code=status.HTTP_200_OK)
def update_driver(id: int, req: DriverUpdateRequest, db: Session = Depends(get_db)):
    """HTTP PATCH: Partially updates metadata details of a driver."""
    driver = DriverService.update_driver(db, id, req)
    data = DriverFrontendResponse.from_orm(driver).model_dump(mode="json")
    return APIResponse.success(
        message="Driver information updated successfully.",
        data={"driver": data},
        status_code=status.HTTP_200_OK
    )

@router.patch("/drivers/{id}/suspend", status_code=status.HTTP_200_OK)
def suspend_driver(id: int, db: Session = Depends(get_db)):
    """HTTP PATCH: Suspends a driver."""
    driver = DriverService.suspend_driver(db, id)
    data = DriverFrontendResponse.from_orm(driver).model_dump(mode="json")
    return APIResponse.success(
        message="Driver suspended successfully.",
        data={"driver": data},
        status_code=status.HTTP_200_OK
    )

@router.patch("/drivers/{id}/activate", status_code=status.HTTP_200_OK)
def activate_driver(id: int, db: Session = Depends(get_db)):
    """HTTP PATCH: Reactivates a suspended driver."""
    driver = DriverService.activate_driver(db, id)
    data = DriverFrontendResponse.from_orm(driver).model_dump(mode="json")
    return APIResponse.success(
        message="Driver activated successfully.",
        data={"driver": data},
        status_code=status.HTTP_200_OK
    )
