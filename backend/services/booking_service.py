import random
from ..models import Appointment
from sqlalchemy.orm import Session

def create_appointment(db: Session, data):
    token = f"HSP-{random.randint(10000, 99999)}"

    appt = Appointment(
        patient_name=data.patient_name,
        phone=data.phone,
        service=data.service,
        doctor=data.doctor,
        appointment_datetime=data.appointment_datetime,
        token=token
    )

    db.add(appt)
    db.commit()
    db.refresh(appt)

    return appt

def get_appointment_by_token(db: Session, token: str):
    return db.query(Appointment).filter(Appointment.token == token).first()

def reschedule_appointment(db: Session, token: str, new_datetime):
    appt = get_appointment_by_token(db, token)
    if appt:
        appt.appointment_datetime = new_datetime
        db.commit()
        db.refresh(appt)
    return appt

def delete_appointment(db: Session, token: str):
    appt = get_appointment_by_token(db, token)
    if appt:
        db.delete(appt)
        db.commit()
        return True
    return False
