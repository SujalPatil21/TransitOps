import os
from datetime import datetime, timedelta
from sqlalchemy.orm import Session
from app.auth.models.models import Role, User
from app.auth.constants import UserRole
from app.auth.services.password_service import PasswordService
from app.modules.fleet.models.vehicle import Vehicle
from app.modules.fleet.models.maintenance import MaintenanceRecord
from app.modules.safety.models.driver import Driver

def seed_roles(db: Session) -> None:
    roles_data = [
        {"name": UserRole.FLEET_MANAGER.value, "description": "Manages vehicle fleets and settings"},
        {"name": UserRole.DISPATCHER.value, "description": "Coordinates trips and schedules drivers"},
        {"name": UserRole.SAFETY_OFFICER.value, "description": "Manages safety checks, maintenance, and compliance audits"},
        {"name": UserRole.FINANCIAL_ANALYST.value, "description": "Monitors expenses, fuel logs, and financial metrics"}
    ]
    for role_info in roles_data:
        existing = db.query(Role).filter_by(name=role_info["name"]).first()
        if not existing:
            new_role = Role(name=role_info["name"], description=role_info["description"])
            db.add(new_role)
    db.commit()

def seed_demo_users(db: Session) -> None:
    users_data = [
        {"username": "fleet_manager", "email": "manager@example.com", "role_name": UserRole.FLEET_MANAGER.value, "name": "Fleet Manager"},
        {"username": "dispatcher", "email": "dispatcher@example.com", "role_name": UserRole.DISPATCHER.value, "name": "Dispatcher"},
        {"username": "safety_officer", "email": "safety@example.com", "role_name": UserRole.SAFETY_OFFICER.value, "name": "Safety Officer"},
        {"username": "financial_analyst", "email": "financial@example.com", "role_name": UserRole.FINANCIAL_ANALYST.value, "name": "Financial Analyst"}
    ]
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

def seed_vehicles_and_maintenance(db: Session) -> None:
    vehicles_data = [
        {"registration_number": "GJ01AB1001", "manufacturer": "Ford",           "model": "Transit",       "vehicle_type": "Van",   "manufacturing_year": 2020, "capacity_kg": 1500,  "odometer": 45000,  "status": "AVAILABLE"},
        {"registration_number": "GJ01AB1002", "manufacturer": "Mercedes-Benz",  "model": "Sprinter",      "vehicle_type": "Van",   "manufacturing_year": 2021, "capacity_kg": 2000,  "odometer": 30000,  "status": "ON_TRIP"},
        {"registration_number": "GJ01AB1003", "manufacturer": "Volvo",          "model": "FH16",          "vehicle_type": "Truck", "manufacturing_year": 2019, "capacity_kg": 18000, "odometer": 120000, "status": "AVAILABLE"},
        {"registration_number": "GJ01AB1004", "manufacturer": "Toyota",         "model": "Hiace",         "vehicle_type": "Van",   "manufacturing_year": 2022, "capacity_kg": 1200,  "odometer": 15000,  "status": "AVAILABLE"},
        {"registration_number": "GJ01AB1005", "manufacturer": "Tata Motors",    "model": "Prima",         "vehicle_type": "Truck", "manufacturing_year": 2018, "capacity_kg": 25000, "odometer": 250000, "status": "IN_SHOP"},
        {"registration_number": "GJ01AB1006", "manufacturer": "Ashok Leyland",  "model": "Dost",          "vehicle_type": "Mini",  "manufacturing_year": 2023, "capacity_kg": 1250,  "odometer": 5000,   "status": "AVAILABLE"},
        {"registration_number": "GJ01AB1007", "manufacturer": "Mahindra",       "model": "Bolero Pik-Up", "vehicle_type": "Mini",  "manufacturing_year": 2021, "capacity_kg": 1700,  "odometer": 60000,  "status": "ON_TRIP"},
        {"registration_number": "GJ01AB1008", "manufacturer": "Eicher",         "model": "Pro 2049",      "vehicle_type": "Truck", "manufacturing_year": 2020, "capacity_kg": 4900,  "odometer": 85000,  "status": "AVAILABLE"},
        {"registration_number": "GJ01AB1009", "manufacturer": "Scania",         "model": "R-Series",      "vehicle_type": "Truck", "manufacturing_year": 2017, "capacity_kg": 30000, "odometer": 350000, "status": "RETIRED"},
        {"registration_number": "GJ01AB1010", "manufacturer": "BharatBenz",     "model": "2823R",         "vehicle_type": "Truck", "manufacturing_year": 2022, "capacity_kg": 28000, "odometer": 40000,  "status": "AVAILABLE"},
        {"registration_number": "GJ01AB1011", "manufacturer": "Isuzu",          "model": "D-Max",         "vehicle_type": "Mini",  "manufacturing_year": 2021, "capacity_kg": 1000,  "odometer": 30000,  "status": "AVAILABLE"},
        {"registration_number": "GJ01AB1012", "manufacturer": "Tata Motors",    "model": "Ace",           "vehicle_type": "Mini",  "manufacturing_year": 2019, "capacity_kg": 750,   "odometer": 90000,  "status": "ON_TRIP"},
        {"registration_number": "GJ01AB1013", "manufacturer": "Ford",           "model": "Transit Custom","vehicle_type": "Van",   "manufacturing_year": 2021, "capacity_kg": 1500,  "odometer": 46000,  "status": "AVAILABLE"},
        {"registration_number": "GJ01AB1014", "manufacturer": "Mercedes-Benz",  "model": "Sprinter 319",  "vehicle_type": "Van",   "manufacturing_year": 2023, "capacity_kg": 2000,  "odometer": 10000,  "status": "AVAILABLE"},
        {"registration_number": "GJ01AB1015", "manufacturer": "Volvo",          "model": "FM",            "vehicle_type": "Truck", "manufacturing_year": 2021, "capacity_kg": 20000, "odometer": 110000, "status": "IN_SHOP"},
    ]
    for v_info in vehicles_data:
        existing = db.query(Vehicle).filter_by(registration_number=v_info["registration_number"]).first()
        if not existing:
            vehicle = Vehicle(**v_info)
            db.add(vehicle)
            db.flush()
            if vehicle.status == "IN_SHOP":
                maintenance = MaintenanceRecord(
                    vehicle_id=vehicle.id,
                    description="Routine scheduled maintenance and oil change",
                    cost=1500.00,
                    start_date=datetime.utcnow() - timedelta(days=2),
                    status="ACTIVE"
                )
                db.add(maintenance)
    db.commit()

def seed_drivers(db: Session) -> None:
    drivers_data = [
        {"employee_id": "EMP001", "full_name": "Ramesh Patel", "email": "ramesh@example.com", "phone": "9876543210", "license_number": "DL101", "license_category": "HMV", "license_expiry": datetime.utcnow() + timedelta(days=500), "experience_years": 10, "safety_score": 95, "status": "AVAILABLE"},
        {"employee_id": "EMP002", "full_name": "Suresh Kumar", "email": "suresh@example.com", "phone": "9876543211", "license_number": "DL102", "license_category": "LMV", "license_expiry": datetime.utcnow() + timedelta(days=300), "experience_years": 5, "safety_score": 88, "status": "ON_TRIP"},
        {"employee_id": "EMP003", "full_name": "Mahesh Sharma", "email": "mahesh@example.com", "phone": "9876543212", "license_number": "DL103", "license_category": "HMV", "license_expiry": datetime.utcnow() + timedelta(days=100), "experience_years": 8, "safety_score": 92, "status": "AVAILABLE"},
        {"employee_id": "EMP004", "full_name": "Rajesh Singh", "email": "rajesh@example.com", "phone": "9876543213", "license_number": "DL104", "license_category": "LMV", "license_expiry": datetime.utcnow() + timedelta(days=600), "experience_years": 3, "safety_score": 85, "status": "OFF_DUTY"},
        {"employee_id": "EMP005", "full_name": "Dinesh Gupta", "email": "dinesh@example.com", "phone": "9876543214", "license_number": "DL105", "license_category": "HMV", "license_expiry": datetime.utcnow() - timedelta(days=10), "experience_years": 15, "safety_score": 98, "status": "SUSPENDED"},
        {"employee_id": "EMP006", "full_name": "Vikram Verma", "email": "vikram@example.com", "phone": "9876543215", "license_number": "DL106", "license_category": "LMV", "license_expiry": datetime.utcnow() + timedelta(days=400), "experience_years": 6, "safety_score": 90, "status": "AVAILABLE"},
        {"employee_id": "EMP007", "full_name": "Anil Desai", "email": "anil@example.com", "phone": "9876543216", "license_number": "DL107", "license_category": "HMV", "license_expiry": datetime.utcnow() + timedelta(days=800), "experience_years": 12, "safety_score": 97, "status": "ON_TRIP"},
        {"employee_id": "EMP008", "full_name": "Sunil Joshi", "email": "sunil@example.com", "phone": "9876543217", "license_number": "DL108", "license_category": "LMV", "license_expiry": datetime.utcnow() + timedelta(days=200), "experience_years": 4, "safety_score": 82, "status": "AVAILABLE"},
        {"employee_id": "EMP009", "full_name": "Prakash Yadav", "email": "prakash@example.com", "phone": "9876543218", "license_number": "DL109", "license_category": "HMV", "license_expiry": datetime.utcnow() + timedelta(days=700), "experience_years": 9, "safety_score": 94, "status": "OFF_DUTY"},
        {"employee_id": "EMP010", "full_name": "Manoj Tiwari", "email": "manoj@example.com", "phone": "9876543219", "license_number": "DL110", "license_category": "LMV", "license_expiry": datetime.utcnow() + timedelta(days=350), "experience_years": 7, "safety_score": 91, "status": "AVAILABLE"},
        {"employee_id": "EMP011", "full_name": "Sanjay Mehta", "email": "sanjay@example.com", "phone": "9876543220", "license_number": "DL111", "license_category": "HMV", "license_expiry": datetime.utcnow() + timedelta(days=450), "experience_years": 11, "safety_score": 96, "status": "ON_TRIP"},
        {"employee_id": "EMP012", "full_name": "Amit Shah", "email": "amit@example.com", "phone": "9876543221", "license_number": "DL112", "license_category": "LMV", "license_expiry": datetime.utcnow() + timedelta(days=250), "experience_years": 5, "safety_score": 89, "status": "AVAILABLE"},
        {"employee_id": "EMP013", "full_name": "Rohit Das", "email": "rohit@example.com", "phone": "9876543222", "license_number": "DL113", "license_category": "HMV", "license_expiry": datetime.utcnow() - timedelta(days=5), "experience_years": 14, "safety_score": 75, "status": "SUSPENDED"},
        {"employee_id": "EMP014", "full_name": "Karan Jain", "email": "karan@example.com", "phone": "9876543223", "license_number": "DL114", "license_category": "LMV", "license_expiry": datetime.utcnow() + timedelta(days=550), "experience_years": 6, "safety_score": 93, "status": "AVAILABLE"},
        {"employee_id": "EMP015", "full_name": "Vivek Bose", "email": "vivek@example.com", "phone": "9876543224", "license_number": "DL115", "license_category": "HMV", "license_expiry": datetime.utcnow() + timedelta(days=900), "experience_years": 13, "safety_score": 99, "status": "AVAILABLE"},
    ]
    for d_info in drivers_data:
        existing = db.query(Driver).filter_by(employee_id=d_info["employee_id"]).first()
        if not existing:
            driver = Driver(**d_info)
            db.add(driver)
    db.commit()

def seed_database(db: Session) -> None:
    """
    Orchestrates the database seeding process.
    """
    seed_roles(db)
    seed_demo_users(db)
    seed_vehicles_and_maintenance(db)
    seed_drivers(db)
