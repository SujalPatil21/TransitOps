import csv
import io
from fastapi import APIRouter, Depends, status, Query
from fastapi.responses import StreamingResponse
from sqlalchemy.orm import Session
from app.database.database import get_db
from app.auth.constants import UserRole
from app.auth.security.permissions import require_roles
from app.common.responses import APIResponse
from app.modules.finance.validators.finance_validator import check_finance_dependencies
from app.modules.finance.services.finance_service import FinanceService

router = APIRouter(
    prefix="/financial",
    tags=["Finance"],
    dependencies=[Depends(require_roles(UserRole.FINANCIAL_ANALYST))]
)

def check_dependencies_or_raise(db: Session):
    """
    Validation helper to assert table dependencies.
    """
    success, error_msg = check_finance_dependencies(db)
    if not success:
        return error_msg
    return None

@router.get("/dashboard")
def get_dashboard(db: Session = Depends(get_db)):
    """
    GET /financial/dashboard
    Returns summary financial metrics and recent trips.
    """
    error_msg = check_dependencies_or_raise(db)
    if error_msg:
        return APIResponse.error(
            message=error_msg,
            error_code="DEPENDENCY_MISSING",
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE
        )
    
    data = FinanceService.get_dashboard_data(db)
    return APIResponse.success(
        message="Financial dashboard retrieved successfully.",
        data=data
    )

@router.get("/analytics")
def get_analytics(
    db: Session = Depends(get_db),
    start_date: str = Query(None, description="Start date (YYYY-MM-DD)"),
    end_date: str = Query(None, description="End date (YYYY-MM-DD)"),
    vehicle_id: int = Query(None, description="Vehicle ID")
):
    """
    GET /financial/analytics
    Returns aggregated metrics for charts based on filters.
    """
    error_msg = check_dependencies_or_raise(db)
    if error_msg:
        return APIResponse.error(
            message=error_msg,
            error_code="DEPENDENCY_MISSING",
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE
        )

    data = FinanceService.get_analytics_data(db, start_date, end_date, vehicle_id)
    return APIResponse.success(
        message="Financial analytics retrieved successfully.",
        data=data
    )

@router.get("/reports")
def get_reports(
    report_type: str = Query(..., description="Report type (fuel, expense, maintenance, vehicle_roi, operational_cost, trip_financial)"),
    db: Session = Depends(get_db)
):
    """
    GET /financial/reports
    Returns a tabular dataset for reporting.
    """
    valid_types = ["fuel", "expense", "maintenance", "vehicle_roi", "operational_cost", "trip_financial"]
    if report_type not in valid_types:
        return APIResponse.error(
            message=f"Invalid report type. Must be one of: {', '.join(valid_types)}",
            error_code="INVALID_REPORT_TYPE",
            status_code=status.HTTP_400_BAD_REQUEST
        )

    error_msg = check_dependencies_or_raise(db)
    if error_msg:
        return APIResponse.error(
            message=error_msg,
            error_code="DEPENDENCY_MISSING",
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE
        )

    data = FinanceService.get_report_data(db, report_type)
    return APIResponse.success(
        message=f"{report_type.replace('_', ' ').title()} Report retrieved successfully.",
        data=data
    )

@router.get("/export/csv")
def export_csv(
    report_type: str = Query(..., description="Report type (fuel, expense, maintenance, vehicle_roi, operational_cost, trip_financial)"),
    db: Session = Depends(get_db)
):
    """
    GET /financial/export/csv
    Streams report data as a CSV download.
    """
    valid_types = ["fuel", "expense", "maintenance", "vehicle_roi", "operational_cost", "trip_financial"]
    if report_type not in valid_types:
        from fastapi import HTTPException
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Invalid report type. Must be one of: {', '.join(valid_types)}"
        )

    error_msg = check_dependencies_or_raise(db)
    if error_msg:
        from fastapi import HTTPException
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail=error_msg
        )

    data = FinanceService.get_report_data(db, report_type)

    output = io.StringIO()
    writer = csv.writer(output)

    if not data:
        writer.writerow(["No records found"])
    else:
        headers = list(data[0].keys())
        writer.writerow([h.replace("_", " ").upper() for h in headers])
        for row in data:
            writer.writerow(list(row.values()))

    output.seek(0)
    response_stream = io.BytesIO(output.getvalue().encode("utf-8"))

    return StreamingResponse(
        response_stream,
        media_type="text/csv",
        headers={"Content-Disposition": f"attachment; filename={report_type}_report.csv"}
    )
