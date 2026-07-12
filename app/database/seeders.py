import os
from sqlalchemy.orm import Session
from app.auth.models.models import Role, User
from app.auth.constants import UserRole
from app.auth.services.password_service import PasswordService

def seed_roles(db: Session) -> None:
    """
    Idempotently seeds the four predefined system roles.
    This roles table is a read-only system reference table.
    """
    roles_data = [
        {"name": UserRole.FLEET_MANAGER.value, "description": "Manages vehicle fleets and settings"},
        {"name": UserRole.DISPATCHER.value, "description": "Coordinates trips and schedules drivers"},
        {"name": UserRole.SAFETY_OFFICER.value, "description": "Manages safety checks, maintenance, and compliance audits"},
        {"name": UserRole.FINANCIAL_ANALYST.value, "description": "Monitors expenses, fuel logs, and financial metrics"}
    ]

    for role_info in roles_data:
        existing = db.query(Role).filter_by(name=role_info["name"]).first()
        if not existing:
            new_role = Role(
                name=role_info["name"],
                description=role_info["description"]
            )
            db.add(new_role)
    db.commit()

def seed_demo_users(db: Session) -> None:
    """
    Idempotently seeds the four development-only demo users.
    """
    users_data = [
        {
            "username": "fleet_manager",
            "email": "manager@example.com",
            "role_name": UserRole.FLEET_MANAGER.value
        },
        {
            "username": "dispatcher",
            "email": "dispatcher@example.com",
            "role_name": UserRole.DISPATCHER.value
        },
        {
            "username": "safety_officer",
            "email": "safety@example.com",
            "role_name": UserRole.SAFETY_OFFICER.value
        },
        {
            "username": "financial_analyst",
            "email": "financial@example.com",
            "role_name": UserRole.FINANCIAL_ANALYST.value
        }
    ]

    # Load password from environment variable, fallback to default
    raw_password = os.getenv("DEMO_USER_PASSWORD", "Password123!")
    password_hash = PasswordService.hash_password(raw_password)

    for user_info in users_data:
        existing = db.query(User).filter_by(email=user_info["email"]).first()
        if not existing:
            role = db.query(Role).filter_by(name=user_info["role_name"]).first()
            if role:
                new_user = User(
                    username=user_info["username"],
                    email=user_info["email"],
                    password_hash=password_hash,
                    role_id=role.id,
                    is_verified=True
                )
                db.add(new_user)
    db.commit()

def seed_database(db: Session) -> None:
    """
    Orchestrates the database seeding process.
    """
    seed_roles(db)
    seed_demo_users(db)
