from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Appointment

# Connect to the database
DATABASE_URL = "sqlite:///./hospital.db"
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(bind=engine)
session = SessionLocal()

# Query all appointments
appointments = session.query(Appointment).all()

print(f"\n--- Found {len(appointments)} Appointments ---\n")
for appt in appointments:
    print(f"ID: {appt.id}")
    print(f"Patient: {appt.patient_name}")
    print(f"Doctor: {appt.doctor}")
    print(f"Service: {appt.service}")
    print(f"Token: {appt.token}")
    print(f"Status: {appt.status}")
    print("-" * 30)

session.close()
