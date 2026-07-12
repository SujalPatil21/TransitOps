from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from app.database.database import get_db
from app.auth.constants import UserRole
from app.auth.security.permissions import require_roles
from app.common.responses import APIResponse
from app.modules.fleet.schemas.request import VehicleCreateRequest, VehicleUpdateRequest, MaintenanceCreateRequest
from app.modules.fleet.schemas.response import VehicleFrontendResponse, MaintenanceFrontendResponse
from app.modules.fleet.services.vehicle_service import VehicleService
from app.modules.fleet.models.maintenance import MaintenanceRecord
from app.modules.fleet.models.vehicle import Vehicle as VehicleModel

# Set up the Fleet module router with role-based restriction
router = APIRouter(
    prefix="/fleet",
    tags=["Fleet"],
    dependencies=[Depends(require_roles(UserRole.FLEET_MANAGER))]
)

@router.post("/vehicles", status_code=status.HTTP_201_CREATED)
def create_vehicle(req: VehicleCreateRequest, db: Session = Depends(get_db)):
    vehicle = VehicleService.create_vehicle(db, req)
    data = VehicleFrontendResponse.from_orm(vehicle).model_dump(mode="json")
    return APIResponse.success(
        message="Vehicle registered successfully.",
        data={"vehicle": data},
        status_code=status.HTTP_201_CREATED
    )

@router.get("/vehicles/{id}", status_code=status.HTTP_200_OK)
def get_vehicle(id: int, db: Session = Depends(get_db)):
    vehicle = VehicleService.get_vehicle_by_id(db, id)
    data = VehicleFrontendResponse.from_orm(vehicle).model_dump(mode="json")
    return APIResponse.success(
        message="Vehicle details retrieved successfully.",
        data={"vehicle": data},
        status_code=status.HTTP_200_OK
    )

@router.get("/vehicles", status_code=status.HTTP_200_OK)
def list_vehicles(db: Session = Depends(get_db)):
    vehicles = VehicleService.list_vehicles(db)
    data = [VehicleFrontendResponse.from_orm(v).model_dump(mode="json") for v in vehicles]
    return APIResponse.success(
        message="Vehicle registry retrieved successfully.",
        data={"vehicles": data},
        status_code=status.HTTP_200_OK
    )

@router.patch("/vehicles/{id}", status_code=status.HTTP_200_OK)
def update_vehicle(id: int, req: VehicleUpdateRequest, db: Session = Depends(get_db)):
    vehicle = VehicleService.update_vehicle(db, id, req)
    data = VehicleFrontendResponse.from_orm(vehicle).model_dump(mode="json")
    return APIResponse.success(
        message="Vehicle information updated successfully.",
        data={"vehicle": data},
        status_code=status.HTTP_200_OK
    )

@router.patch("/vehicles/{id}/retire", status_code=status.HTTP_200_OK)
def retire_vehicle(id: int, db: Session = Depends(get_db)):
    vehicle = VehicleService.retire_vehicle(db, id)
    data = VehicleFrontendResponse.from_orm(vehicle).model_dump(mode="json")
    return APIResponse.success(
        message="Vehicle retired successfully.",
        data={"vehicle": data},
        status_code=status.HTTP_200_OK
    )

@router.get("/maintenance", status_code=status.HTTP_200_OK)
def list_maintenance(db: Session = Depends(get_db)):
    """HTTP GET: Returns all maintenance records joined with vehicle info."""
    records = (
        db.query(MaintenanceRecord, VehicleModel)
        .join(VehicleModel, MaintenanceRecord.vehicle_id == VehicleModel.id)
        .order_by(MaintenanceRecord.start_date.desc())
        .all()
    )
    data = [MaintenanceFrontendResponse.from_orm_joined(m, v).model_dump(mode="json") for m, v in records]
    return APIResponse.success(
        message="Maintenance records retrieved successfully.",
        data={"maintenance_records": data},
        status_code=status.HTTP_200_OK
    )

@router.post("/maintenance", status_code=status.HTTP_201_CREATED)
def create_maintenance(req: MaintenanceCreateRequest, db: Session = Depends(get_db)):
    vehicle, maintenance = VehicleService.send_to_maintenance(db, req.vehicle_id, req.description, req.cost)
    data = MaintenanceFrontendResponse.from_orm_joined(maintenance, vehicle).model_dump(mode="json")
    return APIResponse.success(
        message="Vehicle sent to maintenance.",
        data={"maintenance": data},
        status_code=status.HTTP_201_CREATED
    )
