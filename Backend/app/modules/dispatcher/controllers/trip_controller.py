from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from app.database.database import get_db
from app.common.responses import APIResponse
from app.auth.security.permissions import RoleChecker
from app.modules.dispatcher.schemas.trip import TripCreate, TripUpdate, TripComplete, TripBaseResponse
from app.modules.dispatcher.services.trip_service import TripService
from app.modules.dispatcher.repositories.trip_repository import TripRepository

router = APIRouter(prefix="/dispatcher/trips", tags=["Dispatcher"])

def get_trip_service():
    repo = TripRepository()
    return TripService(repo)

require_dispatcher = RoleChecker(["Dispatcher"])

@router.post("", status_code=status.HTTP_201_CREATED)
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

@router.get("", status_code=status.HTTP_200_OK)
def list_trips(
    db: Session = Depends(get_db),
    service: TripService = Depends(get_trip_service),
    _=Depends(require_dispatcher)
):
    trips = service.list_trips(db)
    trips_data = [TripBaseResponse.model_validate(t).model_dump(mode='json') for t in trips]
    return APIResponse.success(
        message="Trips retrieved successfully.",
        data={"trips": trips_data},
        status_code=status.HTTP_200_OK
    )

@router.get("/{id}", status_code=status.HTTP_200_OK)
def get_trip(
    id: int,
    db: Session = Depends(get_db),
    service: TripService = Depends(get_trip_service),
    _=Depends(require_dispatcher)
):
    trip = service.get_trip(db, id)
    trip_data = TripBaseResponse.model_validate(trip).model_dump(mode='json')
    return APIResponse.success(
        message="Trip retrieved successfully.",
        data={"trip": trip_data},
        status_code=status.HTTP_200_OK
    )

@router.patch("/{id}", status_code=status.HTTP_200_OK)
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

@router.patch("/{id}/dispatch", status_code=status.HTTP_200_OK)
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

@router.patch("/{id}/complete", status_code=status.HTTP_200_OK)
def complete_trip(
    id: int,
    data: TripComplete,
    db: Session = Depends(get_db),
    service: TripService = Depends(get_trip_service),
    _=Depends(require_dispatcher)
):
    trip = service.complete_trip(db, id, data)
    trip_data = TripBaseResponse.model_validate(trip).model_dump(mode='json')
    return APIResponse.success(
        message="Trip completed successfully.",
        data={"trip": trip_data},
        status_code=status.HTTP_200_OK
    )
