import random
from sqlalchemy.orm import Session
from backend.models import Appointment, Patient
from sqlalchemy.exc import IntegrityError

def create_appointment(db: Session, data):
    # 1️⃣ Find or create patient
    patient = db.query(Patient).filter(
        Patient.phone == data.patient_phone
    ).first()

    if not patient:
        patient = Patient(
            name=data.patient_name,
            phone=data.patient_phone
        )
        db.add(patient)
        db.commit()
        db.refresh(patient)

    # 2️⃣ Create appointment
    token = f"HSP-{random.randint(10000,99999)}"

    appointment = Appointment(
        hospital_id=data.hospital_id,
        doctor_id=data.doctor_id,
        patient_id=patient.id,
        appointment_datetime=data.appointment_datetime,
        source=data.source,
        token=token
    )

    db.add(appointment)

    try:
        db.commit()
    except IntegrityError:
        db.rollback()
        raise ValueError("Slot already booked")

    db.refresh(appointment)
    return appointment
