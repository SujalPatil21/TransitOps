from sqlalchemy import inspect
from sqlalchemy.orm import Session
from app.database.database import Base, engine

def check_finance_dependencies(db: Session) -> tuple[bool, str]:
    """
    Checks if the required operational data sources (Trips, Fuel Logs, Expenses, Maintenance, Vehicles)
    are registered in the ORM metadata and their mapped tables exist in the database schema.
    Returns (True, "") if all exist, or (False, "error message") if any is missing.
    """
    try:
        inspector = inspect(engine)
    except Exception:
        return False, "Database connection error."

    mappers = list(Base.registry.mappers)
    
    # Required data concepts and their user-friendly names
    concepts = {
        "Vehicle": "Vehicle",
        "Trip": "Trip",
        "Fuel": "Fuel Log",
        "Expense": "Expense",
        "Maintenance": "Maintenance"
    }
    
    # Track which concepts are found and active in the database
    found = {key: False for key in concepts}
    
    for mapper in mappers:
        class_name = mapper.class_.__name__
        if mapper.local_table is None:
            continue
        table_name = mapper.local_table.name
        
        for key in concepts:
            # Case-sensitive check for the model class name matching the concept
            if key in class_name:
                try:
                    if inspector.has_table(table_name):
                        found[key] = True
                except Exception:
                    pass

    # Validate all requirements
    for key, name in concepts.items():
        if not found[key]:
            return False, f"Dependency missing: {name} table not found in database schema."
            
    return True, ""
