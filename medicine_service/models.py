from sqlalchemy import Column, Integer, String, Float, ForeignKey
from .database import Base

class Medicine(Base):
    __tablename__ = "medicines"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100))
    price = Column(Float)
    description = Column(String(255))

class AppointmentMedicine(Base):
    __tablename__ = "appointment_medicines"
    id = Column(Integer, primary_key=True, index=True)
    appointment_id = Column(Integer)
    medicine_id = Column(Integer)
    quantity = Column(Integer)