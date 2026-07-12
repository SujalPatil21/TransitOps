from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker, DeclarativeBase
from app.config.settings import settings

# Create engine with standard thread connection pooling settings
# pool_pre_ping checks the connection validity before using it, preventing stale connection errors
engine = create_engine(
    settings.DATABASE_URL,
    pool_pre_ping=True,
    pool_size=10,
    max_overflow=20
)

# Session factory configuration
SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)

class Base(DeclarativeBase):
    """
    Modern SQLAlchemy 2.x Declarative Base.
    Inheriting from DeclarativeBase provides proper type-hinting support.
    """
    pass

def get_db():
    """
    FastAPI dependency that yields a database session.
    Guarantees that sessions are always closed properly after execution,
    preventing any database connection leaks.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
