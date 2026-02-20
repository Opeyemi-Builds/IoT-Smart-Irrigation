from sqlalchemy import Column, Integer, String, Float, DateTime, Boolean 
from database import Base
from datetime import datetime

class SensorData(Base):
    __tablename__ = "sensor_data"

    id = Column(Integer, primary_key=True, index=True)
    moisture = Column(Float, nullable=False)
    water_level = Column(Float)  # <-- ADDED: Now the database won't crash when it receives this!
    pump_status = Column(Boolean)
    decision = Column(String)
    timestamp = Column(DateTime, default=datetime.utcnow)