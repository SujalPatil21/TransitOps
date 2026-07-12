import datetime
from sqlalchemy import select, or_, func
from sqlalchemy.orm import Session
from app.modules.safety.models.driver import Driver


class DriverRepository:
    """
    Driver Repository Layer.
    Responsible exclusively for database queries and persistence.
    Contains no business validation, lifecycle checks, or formatting rules.
    """

    @staticmethod
    def create_driver(db: Session, driver: Driver) -> Driver:
        """Adds and persists a new driver to the database."""
        db.add(driver)
        db.commit()
        db.refresh(driver)
        return driver

    @staticmethod
    def update_driver(db: Session, driver: Driver) -> Driver:
        """Saves updates to an existing driver."""
        db.commit()
        db.refresh(driver)
        return driver

    @staticmethod
    def find_by_id(db: Session, driver_id: int) -> Driver | None:
        """Finds a driver by database primary key."""
        stmt = select(Driver).where(Driver.id == driver_id)
        return db.execute(stmt).scalar_one_or_none()

    @staticmethod
    def find_by_employee_id(db: Session, employee_id: str) -> Driver | None:
        """Finds a driver by exact employee ID match."""
        stmt = select(Driver).where(Driver.employee_id == employee_id)
        return db.execute(stmt).scalar_one_or_none()

    @staticmethod
    def find_by_email(db: Session, email: str) -> Driver | None:
        """Finds a driver by exact email match."""
        stmt = select(Driver).where(Driver.email == email)
        return db.execute(stmt).scalar_one_or_none()

    @staticmethod
    def find_by_license(db: Session, license_number: str) -> Driver | None:
        """Finds a driver by exact license number match."""
        stmt = select(Driver).where(Driver.license_number == license_number)
        return db.execute(stmt).scalar_one_or_none()

    @staticmethod
    def list_drivers(db: Session) -> list[Driver]:
        """Lists all drivers in the database."""
        stmt = select(Driver)
        return list(db.execute(stmt).scalars().all())

    @staticmethod
    def search_drivers(db: Session, query: str = None, status_filter: str = None) -> list[Driver]:
        """Searches drivers by name, employee_id, or license_number. Optionally filters by status."""
        stmt = select(Driver)

        if query:
            like_q = f"%{query}%"
            stmt = stmt.where(
                or_(
                    Driver.full_name.ilike(like_q),
                    Driver.employee_id.ilike(like_q),
                    Driver.license_number.ilike(like_q)
                )
            )

        if status_filter:
            stmt = stmt.where(Driver.status == status_filter)

        return list(db.execute(stmt).scalars().all())

    @staticmethod
    def find_expired_licenses(db: Session) -> list[Driver]:
        """Finds drivers whose licenses have expired."""
        now = datetime.datetime.now(datetime.timezone.utc)
        stmt = select(Driver).where(Driver.license_expiry < now)
        return list(db.execute(stmt).scalars().all())

    @staticmethod
    def find_expiring_soon(db: Session, days: int = 30) -> list[Driver]:
        """Finds drivers whose licenses expire within the given number of days."""
        now = datetime.datetime.now(datetime.timezone.utc)
        future = now + datetime.timedelta(days=days)
        stmt = select(Driver).where(
            Driver.license_expiry >= now,
            Driver.license_expiry <= future
        )
        return list(db.execute(stmt).scalars().all())

    @staticmethod
    def count_by_status(db: Session, status_value: str) -> int:
        """Counts drivers with a given status."""
        stmt = select(func.count(Driver.id)).where(Driver.status == status_value)
        return db.execute(stmt).scalar() or 0

    @staticmethod
    def count_total(db: Session) -> int:
        """Counts all drivers."""
        stmt = select(func.count(Driver.id))
        return db.execute(stmt).scalar() or 0

    @staticmethod
    def count_expired_licenses(db: Session) -> int:
        """Counts drivers with expired licenses."""
        now = datetime.datetime.now(datetime.timezone.utc)
        stmt = select(func.count(Driver.id)).where(Driver.license_expiry < now)
        return db.execute(stmt).scalar() or 0

    @staticmethod
    def count_expiring_soon(db: Session, days: int = 30) -> int:
        """Counts drivers whose licenses expire within the given number of days."""
        now = datetime.datetime.now(datetime.timezone.utc)
        future = now + datetime.timedelta(days=days)
        stmt = select(func.count(Driver.id)).where(
            Driver.license_expiry >= now,
            Driver.license_expiry <= future
        )
        return db.execute(stmt).scalar() or 0
