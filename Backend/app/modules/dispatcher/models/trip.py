import datetime
from sqlalchemy import Column, Integer, String, Float, DateTime, Enum, ForeignKey
from sqlalchemy.orm import relationship
from app.database.database import Base
from app.modules.dispatcher.constants import TripStatus

class Trip(Base):
    __tablename__ = "trips"

    id = Column(Integer, primary_key=True, index=True)
    
    # Relationships
    vehicle_id = Column(Integer, ForeignKey("vehicles.id"), nullable=True)
    driver_id = Column(Integer, ForeignKey("drivers.id"), nullable=True)
    
    status = Column(Enum(TripStatus), default=TripStatus.DRAFT, nullable=False)
    cargo_weight_kg = Column(Float, nullable=False)
    
    # Financial data
    trip_revenue = Column(Float, nullable=True)
    
    # Operational data
    fuel_consumed_l = Column(Float, nullable=True)
    fuel_cost = Column(Float, nullable=True)
    toll_charges = Column(Float, nullable=True)
    other_expenses = Column(Float, nullable=True)
    
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.datetime.utcnow, onupdate=datetime.datetime.utcnow)
