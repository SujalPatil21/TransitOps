from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from sqlalchemy import func
from app.database.database import get_db
from app.auth.security.dependencies import get_current_user
from app.common.responses import APIResponse
from app.modules.fleet.models.vehicle import Vehicle
from app.modules.fleet.models.maintenance import MaintenanceRecord
from app.modules.safety.models.driver import Driver

router = APIRouter(
    prefix="/analytics",
    tags=["Analytics"],
    dependencies=[Depends(get_current_user)]
)

@router.get("/kpis", status_code=status.HTTP_200_OK)
def get_kpis(db: Session = Depends(get_db)):
    """
    Returns real-time KPI counts computed from the PostgreSQL database.
    Accessible by any authenticated user.
    """
    # Vehicle KPIs
    total_vehicles = db.query(func.count(Vehicle.id)).scalar() or 0
    available_vehicles = db.query(func.count(Vehicle.id)).filter(Vehicle.status == "AVAILABLE").scalar() or 0
    on_trip_vehicles = db.query(func.count(Vehicle.id)).filter(Vehicle.status == "ON_TRIP").scalar() or 0
    in_shop_vehicles = db.query(func.count(Vehicle.id)).filter(Vehicle.status == "IN_SHOP").scalar() or 0
    retired_vehicles = db.query(func.count(Vehicle.id)).filter(Vehicle.status == "RETIRED").scalar() or 0

    # Driver KPIs
    total_drivers = db.query(func.count(Driver.id)).scalar() or 0
    available_drivers = db.query(func.count(Driver.id)).filter(Driver.status == "AVAILABLE").scalar() or 0
    on_trip_drivers = db.query(func.count(Driver.id)).filter(Driver.status == "ON_TRIP").scalar() or 0
    off_duty_drivers = db.query(func.count(Driver.id)).filter(Driver.status == "OFF_DUTY").scalar() or 0
    suspended_drivers = db.query(func.count(Driver.id)).filter(Driver.status == "SUSPENDED").scalar() or 0

    # Maintenance KPIs
    active_maintenance = db.query(func.count(MaintenanceRecord.id)).filter(MaintenanceRecord.status == "ACTIVE").scalar() or 0
    total_maintenance = db.query(func.count(MaintenanceRecord.id)).scalar() or 0

    # Fleet utilization: (on_trip / total active) * 100
    active_fleet = total_vehicles - retired_vehicles
    fleet_utilization = round((on_trip_vehicles / active_fleet * 100), 1) if active_fleet > 0 else 0

    kpis = {
        # Vehicle
        "totalVehicles": total_vehicles,
        "activeVehicles": total_vehicles - retired_vehicles,
        "availableVehicles": available_vehicles,
        "vehiclesOnTrip": on_trip_vehicles,
        "vehiclesInMaintenance": in_shop_vehicles,
        "retiredVehicles": retired_vehicles,
        # Driver
        "totalDrivers": total_drivers,
        "availableDrivers": available_drivers,
        "driversOnDuty": on_trip_drivers,
        "offDutyDrivers": off_duty_drivers,
        "suspendedDrivers": suspended_drivers,
        # Maintenance
        "activeMaintenance": active_maintenance,
        "totalMaintenance": total_maintenance,
        # Computed
        "fleetUtilization": fleet_utilization,
        # Legacy aliases kept for frontend compatibility
        "activeTrips": on_trip_vehicles,
        "pendingTrips": available_vehicles,
    }

    return APIResponse.success(
        message="KPIs retrieved successfully.",
        data=kpis,
        status_code=status.HTTP_200_OK
    )


@router.get("/roi", status_code=status.HTTP_200_OK)
def get_roi(db: Session = Depends(get_db)):
    """
    Returns per-vehicle ROI summary computed from maintenance costs.
    """
    vehicles = db.query(Vehicle).filter(Vehicle.status != "RETIRED").all()
    result = []
    for v in vehicles:
        total_cost = db.query(func.sum(MaintenanceRecord.cost)).filter(
            MaintenanceRecord.vehicle_id == v.id
        ).scalar() or 0.0
        result.append({
            "vehicle": f"{v.manufacturer} {v.model}",
            "registrationNumber": v.registration_number,
            "totalMaintenanceCost": round(total_cost, 2),
            "status": v.status,
            "odometer": v.odometer,
        })

    return APIResponse.success(
        message="Vehicle ROI data retrieved successfully.",
        data=result,
        status_code=status.HTTP_200_OK
    )
