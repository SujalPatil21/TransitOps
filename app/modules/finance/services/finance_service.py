import datetime
from sqlalchemy import func
from sqlalchemy.orm import Session
from app.database.database import Base

def get_model_class(concept_name: str):
    """
    Dynamically retrieves a model class from Base registry by its name.
    Avoids hardcoding module imports.
    """
    for mapper in Base.registry.mappers:
        class_name = mapper.class_.__name__
        if concept_name in class_name:
            return mapper.class_
    raise ValueError(f"Model for '{concept_name}' not registered in ORM.")

class FinanceService:
    @staticmethod
    def get_dashboard_data(db: Session) -> dict:
        """
        Computes financial dashboard summary metrics dynamically.
        """
        Vehicle = get_model_class("Vehicle")
        Trip = get_model_class("Trip")
        FuelLog = get_model_class("Fuel")
        MaintenanceRecord = get_model_class("Maintenance")

        # 1. Total Fuel Cost
        total_fuel = db.query(func.sum(FuelLog.fuel_cost)).scalar() or 0.0

        # 2. Total Maintenance Cost
        total_maint = db.query(func.sum(MaintenanceRecord.cost)).scalar() or 0.0

        # 3. Total Operational Cost
        total_op = total_fuel + total_maint

        # 4. Average Fuel Efficiency (Distance Travelled / Fuel Consumed)
        # Sum of distance_travelled and fuel_consumed across all trips
        trip_stats = db.query(
            func.sum(Trip.distance_travelled),
            func.sum(Trip.fuel_consumed)
        ).first() or (0.0, 0.0)
        total_dist = trip_stats[0] or 0.0
        total_fuel_cons = trip_stats[1] or 0.0
        avg_efficiency = (total_dist / total_fuel_cons) if total_fuel_cons > 0 else 0.0

        # 5. Fleet Utilization ((Vehicles on Trip / Total Vehicles) * 100)
        total_vehicles = db.query(func.count(Vehicle.id)).scalar() or 0
        vehicles_on_trip = db.query(func.count(Vehicle.id)).filter(
            func.lower(Vehicle.status) == "on_trip"
        ).scalar() or 0
        utilization = (vehicles_on_trip / total_vehicles * 100) if total_vehicles > 0 else 0.0

        # 6. Average Vehicle ROI: (Revenue - (Maintenance Cost + Fuel Cost)) / Acquisition Cost
        # Fetch all vehicles
        vehicles = db.query(Vehicle).all()
        total_roi = 0.0
        roi_count = 0

        for v in vehicles:
            acq_cost = getattr(v, "acquisition_cost", 50000.0) or 50000.0
            if acq_cost <= 0:
                continue

            # Sum revenue for this vehicle
            revenue = db.query(func.sum(Trip.tripRevenue)).filter(Trip.vehicle_id == v.id).scalar() or 0.0
            # Sum fuel for this vehicle
            fuel = db.query(func.sum(FuelLog.fuel_cost)).filter(FuelLog.vehicle_id == v.id).scalar() or 0.0
            # Sum maintenance for this vehicle
            maint = db.query(func.sum(MaintenanceRecord.cost)).filter(MaintenanceRecord.vehicle_id == v.id).scalar() or 0.0

            roi = (revenue - (maint + fuel)) / acq_cost
            total_roi += roi
            roi_count += 1

        avg_roi = (total_roi / roi_count) if roi_count > 0 else 0.0

        # 7. Recent Trips Summary (Last 5 trips)
        recent_trips = db.query(Trip).order_id = Trip.id.desc()
        trips_list = db.query(Trip).order_by(Trip.id.desc()).limit(5).all()
        recent_summary = []
        for t in trips_list:
            veh = db.query(Vehicle).filter(Vehicle.id == t.vehicle_id).first()
            reg = veh.registration_number if veh else "N/A"
            logged_at_str = t.start_time.strftime("%Y-%m-%d %H:%M:%S") if hasattr(t, "start_time") and t.start_time else "N/A"
            recent_summary.append({
                "trip_id": t.id,
                "vehicle_registration": reg,
                "revenue": t.tripRevenue,
                "distance": t.distance_travelled,
                "status": t.status,
                "date": logged_at_str
            })

        return {
            "total_fuel_cost": round(total_fuel, 2),
            "total_maintenance_cost": round(total_maint, 2),
            "total_operational_cost": round(total_op, 2),
            "average_fuel_efficiency": round(avg_efficiency, 2),
            "fleet_utilization": round(utilization, 2),
            "average_vehicle_roi": round(avg_roi, 4),
            "recent_trips_summary": recent_summary,
            "vehicles": [{"id": v.id, "registration": v.registration_number} for v in vehicles],
            "trips": [{"id": t.id, "label": f"Trip #{t.id}"} for t in db.query(Trip).all()]
        }

    @staticmethod
    def get_analytics_data(db: Session, start_date: str = None, end_date: str = None, vehicle_id: int = None) -> dict:
        """
        Computes dynamic analytics filtered by Date Range and Vehicle.
        """
        Vehicle = get_model_class("Vehicle")
        Trip = get_model_class("Trip")
        FuelLog = get_model_class("Fuel")
        MaintenanceRecord = get_model_class("Maintenance")

        # Parse dates
        s_date, e_date = None, None
        if start_date:
            try:
                s_date = datetime.datetime.strptime(start_date, "%Y-%m-%d")
            except ValueError:
                pass
        if end_date:
            try:
                e_date = datetime.datetime.strptime(end_date, "%Y-%m-%d")
            except ValueError:
                pass

        # 1. Fuel Efficiency over time (or per vehicle)
        fuel_query = db.query(FuelLog)
        trip_query = db.query(Trip)
        maint_query = db.query(MaintenanceRecord)

        if vehicle_id:
            fuel_query = fuel_query.filter(FuelLog.vehicle_id == vehicle_id)
            trip_query = trip_query.filter(Trip.vehicle_id == vehicle_id)
            maint_query = maint_query.filter(MaintenanceRecord.vehicle_id == vehicle_id)

        if s_date:
            fuel_query = fuel_query.filter(FuelLog.logged_at >= s_date)
            trip_query = trip_query.filter(Trip.start_time >= s_date)
            maint_query = maint_query.filter(MaintenanceRecord.logged_at >= s_date)

        if e_date:
            fuel_query = fuel_query.filter(FuelLog.logged_at <= e_date)
            trip_query = trip_query.filter(Trip.start_time <= e_date)
            maint_query = maint_query.filter(MaintenanceRecord.logged_at <= e_date)

        # Metrics for selected scope
        fuels = fuel_query.all()
        trips = trip_query.all()
        maints = maint_query.all()

        total_fuel_cost = sum(f.fuel_cost for f in fuels)
        total_fuel_liters = sum(f.fuel_liters for f in fuels)
        total_maint_cost = sum(m.cost for m in maints)
        total_op_cost = total_fuel_cost + total_maint_cost

        total_dist = sum(t.distance_travelled for t in trips)
        total_fuel_cons = sum(t.fuel_consumed for t in trips)
        fuel_efficiency = (total_dist / total_fuel_cons) if total_fuel_cons > 0 else 0.0

        # Fleet utilization
        total_vehicles = db.query(func.count(Vehicle.id)).scalar() or 0
        vehicles_on_trip = db.query(func.count(Vehicle.id)).filter(
            func.lower(Vehicle.status) == "on_trip"
        ).scalar() or 0
        utilization = (vehicles_on_trip / total_vehicles * 100) if total_vehicles > 0 else 0.0

        # ROI for vehicles in scope
        vehicles_query = db.query(Vehicle)
        if vehicle_id:
            vehicles_query = vehicles_query.filter(Vehicle.id == vehicle_id)
        vehicles = vehicles_query.all()

        total_roi = 0.0
        roi_count = 0
        for v in vehicles:
            acq_cost = getattr(v, "acquisition_cost", 50000.0) or 50000.0
            if acq_cost <= 0:
                continue

            revenue = db.query(func.sum(Trip.tripRevenue)).filter(Trip.vehicle_id == v.id)
            if s_date:
                revenue = revenue.filter(Trip.start_time >= s_date)
            if e_date:
                revenue = revenue.filter(Trip.start_time <= e_date)
            rev_val = revenue.scalar() or 0.0

            fuel_c = db.query(func.sum(FuelLog.fuel_cost)).filter(FuelLog.vehicle_id == v.id)
            if s_date:
                fuel_c = fuel_c.filter(FuelLog.logged_at >= s_date)
            if e_date:
                fuel_c = fuel_c.filter(FuelLog.logged_at <= e_date)
            fuel_val = fuel_c.scalar() or 0.0

            maint_c = db.query(func.sum(MaintenanceRecord.cost)).filter(MaintenanceRecord.vehicle_id == v.id)
            if s_date:
                maint_c = maint_c.filter(MaintenanceRecord.logged_at >= s_date)
            if e_date:
                maint_c = maint_c.filter(MaintenanceRecord.logged_at <= e_date)
            maint_val = maint_c.scalar() or 0.0

            roi = (rev_val - (maint_val + fuel_val)) / acq_cost
            total_roi += roi
            roi_count += 1

        avg_roi = (total_roi / roi_count) if roi_count > 0 else 0.0

        return {
            "fuel_efficiency": round(fuel_efficiency, 2),
            "fleet_utilization": round(utilization, 2),
            "operational_cost": round(total_op_cost, 2),
            "vehicle_roi": round(avg_roi, 4),
            "fuel_cost": round(total_fuel_cost, 2),
            "maintenance_cost": round(total_maint_cost, 2)
        }

    @staticmethod
    def get_report_data(db: Session, report_type: str) -> list[dict]:
        """
        Generates dynamic data matrices for specific reports.
        """
        Vehicle = get_model_class("Vehicle")
        Trip = get_model_class("Trip")
        FuelLog = get_model_class("Fuel")
        Expense = get_model_class("Expense")
        MaintenanceRecord = get_model_class("Maintenance")

        records = []

        if report_type == "fuel":
            logs = db.query(FuelLog).all()
            for l in logs:
                v = db.query(Vehicle).filter(Vehicle.id == l.vehicle_id).first()
                reg = v.registration_number if v else "N/A"
                records.append({
                    "id": l.id,
                    "vehicle": reg,
                    "fuel_liters": l.fuel_liters,
                    "fuel_cost": l.fuel_cost,
                    "date": l.logged_at.strftime("%Y-%m-%d %H:%M:%S") if l.logged_at else "N/A"
                })

        elif report_type == "expense":
            exp = db.query(Expense).all()
            for e in exp:
                reg = "N/A"
                if e.vehicle_id:
                    v = db.query(Vehicle).filter(Vehicle.id == e.vehicle_id).first()
                    reg = v.registration_number if v else "N/A"
                records.append({
                    "id": e.id,
                    "vehicle": reg,
                    "amount": e.amount,
                    "category": e.category,
                    "description": e.description or "",
                    "date": e.logged_at.strftime("%Y-%m-%d %H:%M:%S") if e.logged_at else "N/A"
                })

        elif report_type == "maintenance":
            maint = db.query(MaintenanceRecord).all()
            for m in maint:
                v = db.query(Vehicle).filter(Vehicle.id == m.vehicle_id).first()
                reg = v.registration_number if v else "N/A"
                records.append({
                    "id": m.id,
                    "vehicle": reg,
                    "cost": m.cost,
                    "description": m.description or "",
                    "status": getattr(m, "status", "N/A"),
                    "date": m.logged_at.strftime("%Y-%m-%d %H:%M:%S") if m.logged_at else "N/A"
                })

        elif report_type == "vehicle_roi":
            vehicles = db.query(Vehicle).all()
            for v in vehicles:
                acq_cost = getattr(v, "acquisition_cost", 50000.0) or 50000.0
                revenue = db.query(func.sum(Trip.tripRevenue)).filter(Trip.vehicle_id == v.id).scalar() or 0.0
                fuel = db.query(func.sum(FuelLog.fuel_cost)).filter(FuelLog.vehicle_id == v.id).scalar() or 0.0
                maint = db.query(func.sum(MaintenanceRecord.cost)).filter(MaintenanceRecord.vehicle_id == v.id).scalar() or 0.0
                roi = ((revenue - (maint + fuel)) / acq_cost) if acq_cost > 0 else 0.0
                records.append({
                    "vehicle_id": v.id,
                    "registration_number": v.registration_number,
                    "acquisition_cost": acq_cost,
                    "revenue": round(revenue, 2),
                    "fuel_cost": round(fuel, 2),
                    "maintenance_cost": round(maint, 2),
                    "roi": round(roi, 4)
                })

        elif report_type == "operational_cost":
            vehicles = db.query(Vehicle).all()
            for v in vehicles:
                fuel = db.query(func.sum(FuelLog.fuel_cost)).filter(FuelLog.vehicle_id == v.id).scalar() or 0.0
                maint = db.query(func.sum(MaintenanceRecord.cost)).filter(MaintenanceRecord.vehicle_id == v.id).scalar() or 0.0
                records.append({
                    "vehicle_id": v.id,
                    "registration_number": v.registration_number,
                    "fuel_cost": round(fuel, 2),
                    "maintenance_cost": round(maint, 2),
                    "total_operational_cost": round(fuel + maint, 2)
                })

        elif report_type == "trip_financial":
            trips = db.query(Trip).all()
            for t in trips:
                v = db.query(Vehicle).filter(Vehicle.id == t.vehicle_id).first()
                reg = v.registration_number if v else "N/A"
                records.append({
                    "trip_id": t.id,
                    "vehicle": reg,
                    "revenue": t.tripRevenue,
                    "distance": t.distance_travelled,
                    "fuel_consumed": t.fuel_consumed,
                    "status": t.status
                })

        return records
