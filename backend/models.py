from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime

Base = declarative_base()

class Appointment(Base):
    __tablename__ = "appointments"

    id = Column(Integer, primary_key=True)
    patient_name = Column(String, nullable=False)
    phone = Column(String, nullable=False)
    service = Column(String, nullable=False)
    doctor = Column(String, nullable=False)
    appointment_datetime = Column(DateTime, nullable=False)
    token = Column(String, unique=True)
    status = Column(String, default="booked")
    created_at = Column(DateTime, default=datetime.utcnow)
