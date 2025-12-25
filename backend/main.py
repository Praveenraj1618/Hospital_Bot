from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from .database import engine, get_db
from .models import Base
from .schemas import AppointmentCreate, AppointmentResponse
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
