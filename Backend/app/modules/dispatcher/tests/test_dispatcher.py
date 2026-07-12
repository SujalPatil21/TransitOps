import datetime
from decimal import Decimal
import pytest
from pydantic import ValidationError
from app.modules.dispatcher.schemas.trip import TripCreate, TripUpdate
from app.modules.dispatcher.constants import TripStatus
from app.modules.dispatcher.exceptions.exceptions import (
    TripNotDraftException,
    VehicleCapacityExceededException,
    DriverLicenseExpiredException
)

def test_trip_create_validation():
    # Trim checks
    data = TripCreate(
        source="  Warehouse A  ",
        destination="Terminal B  ",
        cargo_weight_kg=1500.0,
        planned_distance=250.0,
        trip_revenue=Decimal("450.00"),
        vehicle_id=1,
        driver_id=2
    )
    assert data.source == "Warehouse A"
    assert data.destination == "Terminal B"

    # Empty checks
    with pytest.raises(ValidationError):
        TripCreate(
            source="   ",
            destination="Terminal B",
            cargo_weight_kg=1500.0,
            planned_distance=250.0,
            trip_revenue=Decimal("450.00"),
            vehicle_id=1,
            driver_id=2
        )

    # Negative cargo weight
    with pytest.raises(ValidationError):
        TripCreate(
            source="Warehouse A",
            destination="Terminal B",
            cargo_weight_kg=-10.0,
            planned_distance=250.0,
            trip_revenue=Decimal("450.00"),
            vehicle_id=1,
            driver_id=2
        )

    # Negative revenue
    with pytest.raises(ValidationError):
        TripCreate(
            source="Warehouse A",
            destination="Terminal B",
            cargo_weight_kg=1500.0,
            planned_distance=250.0,
            trip_revenue=Decimal("-10.00"),
            vehicle_id=1,
            driver_id=2
        )

def test_trip_update_validation():
    data = TripUpdate(source="  New Source  ", trip_revenue=Decimal("500.00"))
    assert data.source == "New Source"
    assert data.trip_revenue == Decimal("500.00")

    with pytest.raises(ValidationError):
        TripUpdate(source="   ")
