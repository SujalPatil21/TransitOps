from sqlalchemy.orm import Session
from app.modules.finance.repositories.finance_repository import FinanceRepository

class FinanceService:
    @staticmethod
    def get_dashboard_data(db: Session) -> dict:
        """
        Computes financial dashboard summary metrics dynamically.
        """
        total_fuel = FinanceRepository.get_total_fuel_cost(db)
        total_maint = FinanceRepository.get_total_maintenance_cost(db)
        total_op = total_fuel + total_maint

        total_dist, total_fuel_cons = FinanceRepository.get_trip_stats(db)
        avg_efficiency = (total_dist / total_fuel_cons) if total_fuel_cons > 0 else 0.0

        total_vehicles = FinanceRepository.get_total_vehicles_count(db)
        vehicles_on_trip = FinanceRepository.get_vehicles_on_trip_count(db)
        utilization = (vehicles_on_trip / total_vehicles * 100) if total_vehicles > 0 else 0.0

        vehicles = FinanceRepository.get_all_vehicles(db)
        total_roi = 0.0
        roi_count = 0

        for v in vehicles:
            acq_cost = getattr(v, "acquisition_cost", 50000.0) or 50000.0
            if acq_cost <= 0:
                continue

            revenue, fuel, maint = FinanceRepository.get_vehicle_financials(db, v.id)
            roi = (revenue - (maint + fuel)) / acq_cost
            total_roi += roi
            roi_count += 1

        avg_roi = (total_roi / roi_count) if roi_count > 0 else 0.0

        trips_list = FinanceRepository.get_recent_trips(db, limit=5)
        recent_summary = []
        for t in trips_list:
            veh = FinanceRepository.get_vehicle_by_id(db, t.vehicle_id)
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
            "trips": [{"id": t.id, "label": f"Trip #{t.id}"} for t in FinanceRepository.get_all_trips(db)]
        }

    @staticmethod
    def get_analytics_data(db: Session, start_date: str = None, end_date: str = None, vehicle_id: int = None) -> dict:
        """
        Computes dynamic analytics filtered by Date Range and Vehicle.
        """
        import datetime
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

        fuels, trips, maints = FinanceRepository.get_analytics_scope_data(db, s_date, e_date, vehicle_id)

        total_fuel_cost = sum(f.fuel_cost for f in fuels)
        total_maint_cost = sum(m.cost for m in maints)
        total_op_cost = total_fuel_cost + total_maint_cost

        total_dist = sum(t.distance_travelled for t in trips)
        total_fuel_cons = sum(t.fuel_consumed for t in trips)
        fuel_efficiency = (total_dist / total_fuel_cons) if total_fuel_cons > 0 else 0.0

        total_vehicles = FinanceRepository.get_total_vehicles_count(db)
        vehicles_on_trip = FinanceRepository.get_vehicles_on_trip_count(db)
        utilization = (vehicles_on_trip / total_vehicles * 100) if total_vehicles > 0 else 0.0

        if vehicle_id:
            vehicles = []
            v = FinanceRepository.get_vehicle_by_id(db, vehicle_id)
            if v:
                vehicles.append(v)
        else:
            vehicles = FinanceRepository.get_all_vehicles(db)

        total_roi = 0.0
        roi_count = 0
        for v in vehicles:
            acq_cost = getattr(v, "acquisition_cost", 50000.0) or 50000.0
            if acq_cost <= 0:
                continue

            revenue, fuel, maint = FinanceRepository.get_vehicle_financials(db, v.id, s_date, e_date)
            roi = (revenue - (maint + fuel)) / acq_cost
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
        records = []

        if report_type == "fuel":
            logs = FinanceRepository.get_report_fuel_logs(db)
            for l in logs:
                v = FinanceRepository.get_vehicle_by_id(db, l.vehicle_id)
                reg = v.registration_number if v else "N/A"
                records.append({
                    "id": l.id,
                    "vehicle": reg,
                    "fuel_liters": l.fuel_liters,
                    "fuel_cost": l.fuel_cost,
                    "date": l.logged_at.strftime("%Y-%m-%d %H:%M:%S") if l.logged_at else "N/A"
                })

        elif report_type == "expense":
            exp = FinanceRepository.get_report_expenses(db)
            for e in exp:
                reg = "N/A"
                if e.vehicle_id:
                    v = FinanceRepository.get_vehicle_by_id(db, e.vehicle_id)
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
            maint = FinanceRepository.get_report_maintenance_records(db)
            for m in maint:
                v = FinanceRepository.get_vehicle_by_id(db, m.vehicle_id)
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
            vehicles = FinanceRepository.get_all_vehicles(db)
            for v in vehicles:
                acq_cost = getattr(v, "acquisition_cost", 50000.0) or 50000.0
                revenue, fuel, maint = FinanceRepository.get_vehicle_financials(db, v.id)
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
            vehicles = FinanceRepository.get_all_vehicles(db)
            for v in vehicles:
                revenue, fuel, maint = FinanceRepository.get_vehicle_financials(db, v.id)
                records.append({
                    "vehicle_id": v.id,
                    "registration_number": v.registration_number,
                    "fuel_cost": round(fuel, 2),
                    "maintenance_cost": round(maint, 2),
                    "total_operational_cost": round(fuel + maint, 2)
                })

        elif report_type == "trip_financial":
            trips = FinanceRepository.get_all_trips(db)
            for t in trips:
                v = FinanceRepository.get_vehicle_by_id(db, t.vehicle_id)
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
