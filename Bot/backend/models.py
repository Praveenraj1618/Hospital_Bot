from sqlalchemy import (
    Column, Integer, String, Boolean, ForeignKey,
    DateTime, Time, UniqueConstraint
)
from sqlalchemy.orm import relationship, declarative_base
from datetime import datetime
from backend.database import engine

Base = declarative_base()

# Company
class Company(Base):
    __tablename__ = "companies"

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

# Hospital
class Hospital(Base):
    __tablename__ = "hospitals"

    id = Column(Integer, primary_key=True)
    company_id = Column(Integer, ForeignKey("companies.id"))
    name = Column(String, nullable=False)
    phone = Column(String)
    address = Column(String)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    doctors = relationship("Doctor", back_populates="hospital")

# HospitalAdmin
class HospitalAdmin(Base):
    __tablename__ = "hospital_admins"

    id = Column(Integer, primary_key=True)
    hospital_id = Column(Integer, ForeignKey("hospitals.id"))
    name = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=False)
    password_hash = Column(String, nullable=False)
    role = Column(String, default="admin")
    created_at = Column(DateTime, default=datetime.utcnow)

# Doctor
class Doctor(Base):
    __tablename__ = "doctors"

    id = Column(Integer, primary_key=True)
    hospital_id = Column(Integer, ForeignKey("hospitals.id"))
    name = Column(String, nullable=False)
    specialization = Column(String, nullable=False)
    qualification = Column(String)
    experience = Column(String)
    consultation_fee = Column(Integer)
    opd_start = Column(Time)
    opd_end = Column(Time)
    slot_minutes = Column(Integer, default=30)
    is_active = Column(Boolean, default=True)

    hospital = relationship("Hospital", back_populates="doctors")

# Patient
class Patient(Base):
    __tablename__ = "patients"

    id = Column(Integer, primary_key=True)
    name = Column(String)
    phone = Column(String, nullable=False)
    email = Column(String)
    created_at = Column(DateTime, default=datetime.utcnow)

# Appointment
class Appointment(Base):
    __tablename__ = "appointments"

    id = Column(Integer, primary_key=True)
    hospital_id = Column(Integer, ForeignKey("hospitals.id"))
    doctor_id = Column(Integer, ForeignKey("doctors.id"))
    patient_id = Column(Integer, ForeignKey("patients.id"))
    appointment_datetime = Column(DateTime, nullable=False)
    status = Column(String, default="booked")
    source = Column(String)
    token = Column(String, unique=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    __table_args__ = (
        UniqueConstraint("doctor_id", "appointment_datetime"),
    )

Base.metadata.create_all(bind=engine)
