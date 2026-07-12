import logging
from contextlib import asynccontextmanager
from fastapi import FastAPI, Request, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.exceptions import RequestValidationError
from sqlalchemy.exc import SQLAlchemyError

from app.config.settings import settings, ConfigurationError
from app.database.database import engine, Base
from app.auth.controllers.router import router as auth_router
from app.modules.fleet.controllers.vehicle_controller import router as fleet_router
from app.modules.fleet.controllers.analytics_controller import router as analytics_router
from app.modules.dispatcher.controllers.trip_controller import router as trip_router
from app.modules.safety.controllers.driver_controller import router as driver_router
from app.auth.exceptions.exceptions import AuthException
from app.common.responses import APIResponse

# Configure structured logging
# ponytail: keep standard logger setup clean and simple in 1 block
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S"
)
logger = logging.getLogger("app.main")

@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Modern lifespan event handler (substitutes deprecated on_event("startup")).
    Automatically logs configuration, checks settings, and initializes SQLAlchemy tables on startup.
    """
    # Log SMTP Configuration on startup
    logger.info(f"SMTP_HOST={settings.SMTP_HOST}")
    logger.info(f"SMTP_PORT={settings.SMTP_PORT}")
    logger.info(f"SMTP_EMAIL={settings.SMTP_EMAIL}")
    logger.info(f"SMTP_PASSWORD_SET={bool(settings.SMTP_PASSWORD)}")

    # Fail fast: validate SMTP configuration
    if not settings.SMTP_EMAIL or not settings.SMTP_PASSWORD:
        raise ConfigurationError("Configuration error: SMTP_EMAIL and SMTP_PASSWORD must be configured.")

    logger.info("Initializing database tables...")
    try:
        from app.auth.models.models import User
        from app.modules.fleet.models.vehicle import Vehicle
        from app.modules.fleet.models.maintenance import MaintenanceRecord
        from app.modules.safety.models.driver import Driver
        from app.modules.dispatcher.models.trip import Trip
        Base.metadata.create_all(bind=engine)
        logger.info("Database tables initialized successfully.")
        
        # Idempotently seed system roles and demo users
        from app.database.seeders import seed_database
        from app.database.database import SessionLocal
        db = SessionLocal()
        try:
            seed_database(db)
            logger.info("Database seeded successfully.")
        finally:
            db.close()
    except Exception as e:
        logger.error(f"[ERROR] Failed to initialize database tables: {str(e)}")
        # We do not crash startup in case DB is momentarily unavailable, but log it clearly.
    
    yield
    
    logger.info("Shutting down application...")


# Initialize FastAPI application
app = FastAPI(
    title=settings.PROJECT_NAME,
    description="Reusable Production-Grade Authentication Module",
    version="1.0.0",
    lifespan=lifespan
)

# CORS Configuration
# Essential for decoupling and cross-origin frontend communication (e.g. SPAs, Hackathons)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Restrict this to trusted domains in production settings
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Register Authentication router
app.include_router(auth_router)
app.include_router(fleet_router)
app.include_router(analytics_router)
app.include_router(trip_router)
app.include_router(driver_router)

# Mount the test front-end static files
# static folder is at the root of the workspace
import os
static_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "static")
if os.path.exists(static_path):
    app.mount("/static", StaticFiles(directory=static_path), name="static")

@app.get("/")
def read_root():
    """
    Redirects root requests to the test HTML frontend.
    """
    from fastapi.responses import RedirectResponse
    return RedirectResponse(url="/static/index.html")

@app.get("/fleet-manager/dashboard")
@app.get("/dispatcher/dashboard")
@app.get("/safety-officer/dashboard")
@app.get("/financial-analyst/dashboard")
def dashboard_fallback():
    from fastapi.responses import FileResponse
    import os
    static_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "static")
    return FileResponse(os.path.join(static_path, "index.html"))


# ==============================================================================
# GLOBAL EXCEPTION HANDLERS (SOLID Architecture & Security)
# ==============================================================================

@app.exception_handler(AuthException)
async def auth_exception_handler(request: Request, exc: AuthException):
    """
    Catches application-specific domain exceptions and returns client-friendly JSON.
    """
    return APIResponse.error(
        message=exc.message,
        error_code=exc.error_code,
        status_code=exc.status_code,
        data=exc.data
    )


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    """
    Intercepts Pydantic model validation errors (HTTP 422) and returns a clean, uniform payload.
    """
    errors = []
    for error in exc.errors():
        # Clean path details to make them user readable
        field = " -> ".join([str(p) for p in error.get("loc", []) if p != "body"])
        message = error.get("msg")
        errors.append({"field": field, "message": message})
    
    # Custom message representing the first validation failure
    first_error_msg = f"Validation failed: {errors[0]['message']} on field '{errors[0]['field']}'" if errors else "Validation failed."
    
    return APIResponse.error(
        message=first_error_msg,
        error_code="VALIDATION_ERROR",
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        data={"errors": errors}
    )


@app.exception_handler(SQLAlchemyError)
async def database_exception_handler(request: Request, exc: SQLAlchemyError):
    """
    Prevents raw database stack traces or SQL code injections from leaking to client.
    """
    logger.error(f"[ERROR] Database exception occurred: {str(exc)}", exc_info=True)
    return APIResponse.error(
        message="A database error occurred. Please try again later.",
        error_code="DATABASE_ERROR",
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR
    )


@app.exception_handler(Exception)
async def general_exception_handler(request: Request, exc: Exception):
    """
    Catches all other unexpected system failures, logging the details internally and masking them.
    """
    logger.error(f"[ERROR] Unhandled system exception: {str(exc)}", exc_info=True)
    return APIResponse.error(
        message="An unexpected system error occurred. Please contact support.",
        error_code="INTERNAL_SERVER_ERROR",
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR
    )
