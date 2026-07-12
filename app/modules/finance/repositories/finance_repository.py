from sqlalchemy import func
from sqlalchemy.orm import Session
from app.database.database import Base

def get_model_class(concept_name: str):
    """
    Dynamically retrieves a model class from Base registry by its name.
    """
    for mapper in Base.registry.mappers:
        class_name = mapper.class_.__name__
        if concept_name in class_name:
            return mapper.class_
    raise ValueError(f"Model for '{concept_name}' not registered in ORM.")

class FinanceRepository:
    """
    Finance Repository Layer.
    Encapsulates all database query operations.
    Only performs read queries. No writes, commits, updates, or deletes.
    """

    @staticmethod
    def get_total_fuel_cost(db: Session) -> float:
        FuelLog = get_model_class("Fuel")
        return db.query(func.sum(FuelLog.fuel_cost)).scalar() or 0.0

    @staticmethod
    def get_total_maintenance_cost(db: Session) -> float:
        MaintenanceRecord = get_model_class("Maintenance")
        return db.query(func.sum(MaintenanceRecord.cost)).scalar() or 0.0

    @staticmethod
    def get_trip_stats(db: Session) -> tuple[float, float]:
        Trip = get_model_class("Trip")
        stats = db.query(
            func.sum(Trip.distance_travelled),
            func.sum(Trip.fuel_consumed)
        ).first() or (0.0, 0.0)
        return stats[0] or 0.0, stats[1] or 0.0

    @staticmethod
    def get_total_vehicles_count(db: Session) -> int:
        Vehicle = get_model_class("Vehicle")
        return db.query(func.count(Vehicle.id)).scalar() or 0

    @staticmethod
    def get_vehicles_on_trip_count(db: Session) -> int:
        Vehicle = get_model_class("Vehicle")
        return db.query(func.count(Vehicle.id)).filter(
            func.lower(Vehicle.status) == "on_trip"
        ).scalar() or 0

    @staticmethod
    def get_all_vehicles(db: Session) -> list:
        Vehicle = get_model_class("Vehicle")
        return db.query(Vehicle).all()

    @staticmethod
    def get_all_trips(db: Session) -> list:
        Trip = get_model_class("Trip")
        return db.query(Trip).all()

    @staticmethod
    def get_vehicle_financials(db: Session, vehicle_id: int, start_date=None, end_date=None) -> tuple[float, float, float]:
        Trip = get_model_class("Trip")
        FuelLog = get_model_class("Fuel")
        MaintenanceRecord = get_model_class("Maintenance")

        # Revenue
        rev_q = db.query(func.sum(Trip.tripRevenue)).filter(Trip.vehicle_id == vehicle_id)
        if start_date:
            rev_q = rev_q.filter(Trip.start_time >= start_date)
        if end_date:
            rev_q = rev_q.filter(Trip.start_time <= end_date)
        revenue = rev_q.scalar() or 0.0

        # Fuel cost
        fuel_q = db.query(func.sum(FuelLog.fuel_cost)).filter(FuelLog.vehicle_id == vehicle_id)
        if start_date:
            fuel_q = fuel_q.filter(FuelLog.logged_at >= start_date)
        if end_date:
            fuel_q = fuel_q.filter(FuelLog.logged_at <= end_date)
        fuel = fuel_q.scalar() or 0.0

        # Maintenance cost
        maint_q = db.query(func.sum(MaintenanceRecord.cost)).filter(MaintenanceRecord.vehicle_id == vehicle_id)
        if start_date:
            maint_q = maint_q.filter(MaintenanceRecord.logged_at >= start_date)
        if end_date:
            maint_q = maint_q.filter(MaintenanceRecord.logged_at <= end_date)
        maint = maint_q.scalar() or 0.0

        return revenue, fuel, maint

    @staticmethod
    def get_recent_trips(db: Session, limit: int = 5) -> list:
        Trip = get_model_class("Trip")
        return db.query(Trip).order_by(Trip.id.desc()).limit(limit).all()

    @staticmethod
    def get_vehicle_by_id(db: Session, vehicle_id: int):
        Vehicle = get_model_class("Vehicle")
        return db.query(Vehicle).filter(Vehicle.id == vehicle_id).first()

    @staticmethod
    def get_analytics_scope_data(db: Session, start_date=None, end_date=None, vehicle_id: int = None) -> tuple[list, list, list]:
        Trip = get_model_class("Trip")
        FuelLog = get_model_class("Fuel")
        MaintenanceRecord = get_model_class("Maintenance")

        fuel_q = db.query(FuelLog)
        trip_q = db.query(Trip)
        maint_q = db.query(MaintenanceRecord)

        if vehicle_id:
            fuel_q = fuel_q.filter(FuelLog.vehicle_id == vehicle_id)
            trip_q = trip_q.filter(Trip.vehicle_id == vehicle_id)
            maint_q = maint_q.filter(MaintenanceRecord.vehicle_id == vehicle_id)

        if start_date:
            fuel_q = fuel_q.filter(FuelLog.logged_at >= start_date)
            trip_q = trip_q.filter(Trip.start_time >= start_date)
            maint_q = maint_q.filter(MaintenanceRecord.logged_at >= start_date)

        if end_date:
            fuel_q = fuel_q.filter(FuelLog.logged_at <= end_date)
            trip_q = trip_q.filter(Trip.start_time <= end_date)
            maint_q = maint_q.filter(MaintenanceRecord.logged_at <= end_date)

        return fuel_q.all(), trip_q.all(), maint_q.all()

    @staticmethod
    def get_report_fuel_logs(db: Session) -> list:
        FuelLog = get_model_class("Fuel")
        return db.query(FuelLog).all()

    @staticmethod
    def get_report_expenses(db: Session) -> list:
        Expense = get_model_class("Expense")
        return db.query(Expense).all()

    @staticmethod
    def get_report_maintenance_records(db: Session) -> list:
        MaintenanceRecord = get_model_class("Maintenance")
        return db.query(MaintenanceRecord).all()
