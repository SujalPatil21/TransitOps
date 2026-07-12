import datetime
from sqlalchemy import String, Float, Integer, DateTime
from sqlalchemy.orm import Mapped, mapped_column
from app.database.database import Base
from app.modules.fleet.constants import VehicleStatus

def get_utc_now() -> datetime.datetime:
    return datetime.datetime.now(datetime.timezone.utc)

class Vehicle(Base):
    """
    SQLAlchemy Vehicle Model.
    Stores metadata, capacity, odometer, and lifecycle status for each vehicle in the registry.
    Enforces a database-level UNIQUE constraint on registration_number.
    """
    __tablename__ = "vehicles"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    registration_number: Mapped[str] = mapped_column(String(50), unique=True, nullable=False, index=True)
    vehicle_type: Mapped[str] = mapped_column(String(50), nullable=False)
    manufacturer: Mapped[str] = mapped_column(String(100), nullable=False)
    model: Mapped[str] = mapped_column(String(100), nullable=False)
    manufacturing_year: Mapped[int] = mapped_column(Integer, nullable=False)
    capacity_kg: Mapped[float] = mapped_column(Float, nullable=False)
    odometer: Mapped[float] = mapped_column(Float, nullable=False)
    acquisition_cost: Mapped[float] = mapped_column(Float, default=50000.0, nullable=False)
    status: Mapped[str] = mapped_column(String(50), default=VehicleStatus.AVAILABLE.value, nullable=False)
    
    created_at: Mapped[datetime.datetime] = mapped_column(
        DateTime(timezone=True), 
        default=get_utc_now, 
        nullable=False
    )
    updated_at: Mapped[datetime.datetime] = mapped_column(
        DateTime(timezone=True), 
        default=get_utc_now, 
        onupdate=get_utc_now, 
        nullable=False
    )
