import datetime
from sqlalchemy import String, Float, Integer, DateTime, ForeignKey, CheckConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.database.database import Base

def get_utc_now() -> datetime.datetime:
    return datetime.datetime.now(datetime.timezone.utc)

class MaintenanceRecord(Base):
    """
    SQLAlchemy Maintenance Record Model.
    Tracks vehicle maintenance activities.
    """
    __tablename__ = "maintenance_records"
    __table_args__ = (
        CheckConstraint('cost >= 0', name='check_maintenance_cost_non_negative'),
    )

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    vehicle_id: Mapped[int] = mapped_column(ForeignKey("vehicles.id"), nullable=False, index=True)
    description: Mapped[str] = mapped_column(String(255), nullable=False)
    
    start_date: Mapped[datetime.datetime] = mapped_column(DateTime(timezone=True), nullable=False, default=get_utc_now)
    end_date: Mapped[datetime.datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    
    cost: Mapped[float] = mapped_column(Float, nullable=False, default=0.0)
    status: Mapped[str] = mapped_column(String(50), default="ACTIVE", nullable=False, index=True)
    
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

    # Relationship
    vehicle = relationship("Vehicle", backref="maintenance_records")
