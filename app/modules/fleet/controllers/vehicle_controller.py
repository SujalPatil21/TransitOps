from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from app.database.database import get_db
from app.auth.constants import UserRole
from app.auth.security.permissions import require_roles
from app.common.responses import APIResponse
from app.modules.fleet.schemas.request import VehicleCreateRequest, VehicleUpdateRequest
from app.modules.fleet.schemas.response import VehicleResponse
from app.modules.fleet.services.vehicle_service import VehicleService

# Set up the Fleet module router with role-based restriction
router = APIRouter(
    prefix="/fleet",
    tags=["Fleet"],
    dependencies=[Depends(require_roles(UserRole.FLEET_MANAGER))]
)

@router.post("/vehicles", status_code=status.HTTP_201_CREATED)
def create_vehicle(req: VehicleCreateRequest, db: Session = Depends(get_db)):
    """
    HTTP POST: Registers a new vehicle in the system.
    """
    vehicle = VehicleService.create_vehicle(db, req)
    data = VehicleResponse.model_validate(vehicle).model_dump(mode="json")
    return APIResponse.success(
        message="Vehicle registered successfully.",
        data={"vehicle": data},
        status_code=status.HTTP_201_CREATED
    )

@router.get("/vehicles/{id}", status_code=status.HTTP_200_OK)
def get_vehicle(id: int, db: Session = Depends(get_db)):
    """
    HTTP GET: Retrieves details for a specific vehicle by database ID.
    """
    vehicle = VehicleService.get_vehicle_by_id(db, id)
    data = VehicleResponse.model_validate(vehicle).model_dump(mode="json")
    return APIResponse.success(
        message="Vehicle details retrieved successfully.",
        data={"vehicle": data},
        status_code=status.HTTP_200_OK
    )

@router.get("/vehicles", status_code=status.HTTP_200_OK)
def list_vehicles(db: Session = Depends(get_db)):
    """
    HTTP GET: Retrieves a list of all registered vehicles.
    """
    vehicles = VehicleService.list_vehicles(db)
    data = [VehicleResponse.model_validate(v).model_dump(mode="json") for v in vehicles]
    return APIResponse.success(
        message="Vehicle registry retrieved successfully.",
        data={"vehicles": data},
        status_code=status.HTTP_200_OK
    )

@router.patch("/vehicles/{id}", status_code=status.HTTP_200_OK)
def update_vehicle(id: int, req: VehicleUpdateRequest, db: Session = Depends(get_db)):
    """
    HTTP PATCH: Partially updates metadata details of a vehicle.
    """
    vehicle = VehicleService.update_vehicle(db, id, req)
    data = VehicleResponse.model_validate(vehicle).model_dump(mode="json")
    return APIResponse.success(
        message="Vehicle information updated successfully.",
        data={"vehicle": data},
        status_code=status.HTTP_200_OK
    )

@router.patch("/vehicles/{id}/retire", status_code=status.HTTP_200_OK)
def retire_vehicle(id: int, db: Session = Depends(get_db)):
    """
    HTTP PATCH: Marks a vehicle as retired (Irreversible).
    """
    vehicle = VehicleService.retire_vehicle(db, id)
    data = VehicleResponse.model_validate(vehicle).model_dump(mode="json")
    return APIResponse.success(
        message="Vehicle retired successfully.",
        data={"vehicle": data},
        status_code=status.HTTP_200_OK
    )
