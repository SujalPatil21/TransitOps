import datetime
from sqlalchemy import ForeignKey, String, Boolean, DateTime
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.database.database import Base
from app.auth.constants import UserRole

# Default function for timezone-aware UTC datetime
# ponytail: keep standard library utcnow alternative simple and compliant with Python 3.12+
def get_utc_now() -> datetime.datetime:
    return datetime.datetime.now(datetime.timezone.utc)

class Role(Base):
    """
    SQLAlchemy Role Model.
    Supports system-defined Fleet Manager, Dispatcher, Safety Officer, and Financial Analyst roles.
    """
    __tablename__ = "roles"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(50), unique=True, nullable=False, index=True)
    description: Mapped[str | None] = mapped_column(String(200), nullable=True)
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

    # Relationships
    users: Mapped[list["User"]] = relationship(back_populates="role")


class User(Base):
    """
    SQLAlchemy User Model.
    Uses modern 2.0 type annotated mapping style.
    """
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    username: Mapped[str] = mapped_column(String(50), unique=True, nullable=False, index=True)
    email: Mapped[str] = mapped_column(String(100), unique=True, nullable=False, index=True)
    password_hash: Mapped[str] = mapped_column(String(255), nullable=False)
    
    role_id: Mapped[int] = mapped_column(ForeignKey("roles.id"), nullable=False)
    is_verified: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    
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

    # Relationships
    role: Mapped["Role"] = relationship(back_populates="users")
    # If a user is deleted, all their OTP records are deleted automatically
    otps: Mapped[list["OTPVerification"]] = relationship(
        back_populates="user", 
        cascade="all, delete-orphan"
    )



class OTPVerification(Base):
    """
    SQLAlchemy OTP Verification Model.
    Stores securely hashed OTPs mapped to purpose and expiry.
    """
    __tablename__ = "otp_verifications"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE"), 
        nullable=False
    )
    purpose: Mapped[str] = mapped_column(String(50), nullable=False)
    otp_hash: Mapped[str] = mapped_column(String(255), nullable=False)
    
    expires_at: Mapped[datetime.datetime] = mapped_column(
        DateTime(timezone=True), 
        nullable=False
    )
    created_at: Mapped[datetime.datetime] = mapped_column(
        DateTime(timezone=True), 
        default=get_utc_now, 
        nullable=False
    )

    # Relationships
    user: Mapped["User"] = relationship(back_populates="otps")
