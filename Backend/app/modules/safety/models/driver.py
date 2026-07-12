import datetime
from sqlalchemy import String, Float, Integer, DateTime
from sqlalchemy.orm import Mapped, mapped_column
from app.database.database import Base
from app.modules.safety.constants import DriverStatus

def get_utc_now() -> datetime.datetime:
    return datetime.datetime.now(datetime.timezone.utc)

class Driver(Base):
    """
    SQLAlchemy Driver Model.
    Stores driver registry, compliance, and license information.
    Enforces database-level UNIQUE constraints on employee_id, email, and license_number.
    """
    __tablename__ = "drivers"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    employee_id: Mapped[str] = mapped_column(String(50), unique=True, nullable=False, index=True)
    full_name: Mapped[str] = mapped_column(String(150), nullable=False)
    email: Mapped[str] = mapped_column(String(150), unique=True, nullable=False, index=True)
    phone: Mapped[str] = mapped_column(String(20), nullable=False)
    license_number: Mapped[str] = mapped_column(String(50), unique=True, nullable=False, index=True)
    license_category: Mapped[str] = mapped_column(String(20), nullable=False)
    license_expiry: Mapped[datetime.datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    experience_years: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    safety_score: Mapped[float] = mapped_column(Float, nullable=False, default=100.0)
    status: Mapped[str] = mapped_column(String(50), default=DriverStatus.AVAILABLE.value, nullable=False)

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
