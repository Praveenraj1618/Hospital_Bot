from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from .database import engine, get_db
from .models import Base
from .schemas import AppointmentCreate, AppointmentResponse, AppointmentDetail
from .services.booking_service import create_appointment
from .services.telegram_service import notify_user

Base.metadata.create_all(bind=engine)

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)

@app.post("/api/appointments", response_model=AppointmentResponse)
def book(payload: AppointmentCreate, db: Session = Depends(get_db)):
    appt = create_appointment(db, payload)
    notify_user(payload.phone, appt)
    return {"token": appt.token, "status": appt.status}

@app.get("/api/appointments/{token}", response_model=AppointmentDetail)
def get_appointment(token: str, db: Session = Depends(get_db)):
    from .models import Appointment
    appt = db.query(Appointment).filter(Appointment.token == token).first()
    if not appt:
        from fastapi import HTTPException
        raise HTTPException(status_code=404, detail="Appointment not found")
    return appt

@app.delete("/api/appointments/{token}")
def cancel_appointment(token: str, db: Session = Depends(get_db)):
    from .models import Appointment
    from fastapi import HTTPException
    
    appt = db.query(Appointment).filter(Appointment.token == token).first()
    if not appt:
        raise HTTPException(status_code=404, detail="Appointment not found")
    
    appt.status = "cancelled"
    db.commit()
    return {"status": "cancelled"}

@app.patch("/api/appointments/{token}/reschedule")
def reschedule(token: str, new_datetime: str, db: Session = Depends(get_db)):
    from .models import Appointment
    from fastapi import HTTPException
    from datetime import datetime
    
    appt = db.query(Appointment).filter(Appointment.token == token).first()
    if not appt:
        raise HTTPException(status_code=404, detail="Appointment not found")

    if appt.status == "cancelled":
        raise HTTPException(status_code=400, detail="Appointment already cancelled")

    # Parse string back to datetime if passed as query param string
    if isinstance(new_datetime, str):
        new_datetime = datetime.fromisoformat(new_datetime)

    appt.appointment_datetime = new_datetime
    appt.status = "rescheduled"
    db.commit()

    return {"status": "rescheduled", "new_datetime": new_datetime}
