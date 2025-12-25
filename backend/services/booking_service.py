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
