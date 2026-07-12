import datetime
from decimal import Decimal
from sqlalchemy import String, Numeric, DateTime, ForeignKey, Enum, CheckConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.database.database import Base
from app.modules.dispatcher.constants import TripStatus

def get_utc_now() -> datetime.datetime:
    return datetime.datetime.now(datetime.timezone.utc)

class Trip(Base):
    """
    SQLAlchemy Trip Model.
    Represents the operational details of a shipment lifecycle.
    """
    __tablename__ = "trips"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    source: Mapped[str] = mapped_column(String(255), nullable=False)
    destination: Mapped[str] = mapped_column(String(255), nullable=False)
    cargo_weight_kg: Mapped[float] = mapped_column(nullable=False)
    planned_distance: Mapped[float] = mapped_column(nullable=False)
    trip_revenue: Mapped[Decimal] = mapped_column(Numeric(12, 2), nullable=False)
    
    vehicle_id: Mapped[int] = mapped_column(ForeignKey("vehicles.id", ondelete="RESTRICT"), nullable=False)
    driver_id: Mapped[int] = mapped_column(ForeignKey("drivers.id", ondelete="RESTRICT"), nullable=False)
    
    status: Mapped[TripStatus] = mapped_column(Enum(TripStatus), default=TripStatus.DRAFT, nullable=False)
    
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

    # Relationships to avoid duplicate database attributes
    vehicle = relationship("Vehicle")
    driver = relationship("Driver")

    __table_args__ = (
        CheckConstraint("cargo_weight_kg > 0", name="chk_trip_cargo_weight_positive"),
        CheckConstraint("planned_distance > 0", name="chk_trip_distance_positive"),
        CheckConstraint("trip_revenue >= 0", name="chk_trip_revenue_nonnegative"),
    )
