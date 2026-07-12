from typing import Optional
from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.orm import Session
from app.database.database import get_db
from app.common.responses import APIResponse
from app.auth.security.permissions import RoleChecker
from app.modules.dispatcher.schemas.trip import TripCreate, TripUpdate, TripBaseResponse
from app.modules.dispatcher.services.trip_service import TripService
from app.modules.dispatcher.repositories.trip_repository import TripRepository
from app.modules.fleet.schemas.response import VehicleResponse
from app.modules.safety.schemas.response import DriverFrontendResponse

# Create the router
router = APIRouter(prefix="/dispatcher", tags=["Dispatcher"])

def get_trip_service():
    repo = TripRepository()
    return TripService(repo)

require_dispatcher = RoleChecker(["Dispatcher"])
require_read = RoleChecker(["Dispatcher", "Safety Officer"])

@router.post("/trips", status_code=status.HTTP_201_CREATED)
def create_trip(
    data: TripCreate, 
    db: Session = Depends(get_db), 
    service: TripService = Depends(get_trip_service),
    _=Depends(require_dispatcher)
):
    trip = service.create_trip(db, data)
    trip_data = TripBaseResponse.model_validate(trip).model_dump(mode='json')
    return APIResponse.success(
        message="Trip created successfully.",
        data={"trip": trip_data},
        status_code=status.HTTP_201_CREATED
    )

@router.get("/trips", status_code=status.HTTP_200_OK)
def list_trips(
    db: Session = Depends(get_db),
    service: TripService = Depends(get_trip_service),
    _=Depends(require_read)
):
    trips = service.list_trips(db)
    trips_data = [TripBaseResponse.model_validate(t).model_dump(mode='json') for t in trips]
    return APIResponse.success(
        message="Trips retrieved successfully.",
        data={"trips": trips_data},
        status_code=status.HTTP_200_OK
    )

@router.get("/trips/{id}", status_code=status.HTTP_200_OK)
def get_trip(
    id: int,
    db: Session = Depends(get_db),
    service: TripService = Depends(get_trip_service),
    _=Depends(require_read)
):
    trip = service.get_trip(db, id)
    trip_data = TripBaseResponse.model_validate(trip).model_dump(mode='json')
    return APIResponse.success(
        message="Trip retrieved successfully.",
        data={"trip": trip_data},
        status_code=status.HTTP_200_OK
    )

@router.patch("/trips/{id}", status_code=status.HTTP_200_OK)
def update_draft(
    id: int,
    data: TripUpdate,
    db: Session = Depends(get_db),
    service: TripService = Depends(get_trip_service),
    _=Depends(require_dispatcher)
):
    trip = service.update_draft(db, id, data)
    trip_data = TripBaseResponse.model_validate(trip).model_dump(mode='json')
    return APIResponse.success(
        message="Draft trip updated successfully.",
        data={"trip": trip_data},
        status_code=status.HTTP_200_OK
    )

@router.post("/trips/{id}/dispatch", status_code=status.HTTP_200_OK)
def dispatch_trip(
    id: int,
    db: Session = Depends(get_db),
    service: TripService = Depends(get_trip_service),
    _=Depends(require_dispatcher)
):
    trip = service.dispatch_trip(db, id)
    trip_data = TripBaseResponse.model_validate(trip).model_dump(mode='json')
    return APIResponse.success(
        message="Trip dispatched successfully.",
        data={"trip": trip_data},
        status_code=status.HTTP_200_OK
    )

@router.post("/trips/{id}/complete", status_code=status.HTTP_200_OK)
def complete_trip(
    id: int,
    db: Session = Depends(get_db),
    service: TripService = Depends(get_trip_service),
    _=Depends(require_dispatcher)
):
    trip = service.complete_trip(db, id)
    trip_data = TripBaseResponse.model_validate(trip).model_dump(mode='json')
    return APIResponse.success(
        message="Trip completed successfully.",
        data={"trip": trip_data},
        status_code=status.HTTP_200_OK
    )

@router.get("/eligible-vehicles", status_code=status.HTTP_200_OK)
def get_eligible_vehicles(
    cargo_weight_kg: Optional[float] = Query(None, gt=0),
    db: Session = Depends(get_db),
    service: TripService = Depends(get_trip_service),
    _=Depends(require_dispatcher)
):
    vehicles = service.list_eligible_vehicles(db, cargo_weight_kg)
    vehicles_data = [VehicleResponse.model_validate(v).model_dump(mode='json') for v in vehicles]
    return APIResponse.success(
        message="Eligible vehicles retrieved successfully.",
        data={"vehicles": vehicles_data},
        status_code=status.HTTP_200_OK
    )

@router.get("/eligible-drivers", status_code=status.HTTP_200_OK)
def get_eligible_drivers(
    db: Session = Depends(get_db),
    service: TripService = Depends(get_trip_service),
    _=Depends(require_dispatcher)
):
    drivers = service.list_eligible_drivers(db)
    drivers_data = [DriverFrontendResponse.from_orm(d).model_dump(mode='json') for d in drivers]
    return APIResponse.success(
        message="Eligible drivers retrieved successfully.",
        data={"drivers": drivers_data},
        status_code=status.HTTP_200_OK
    )
