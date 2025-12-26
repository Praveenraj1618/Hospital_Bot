from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from .database import engine, get_db
from .models import Base
from .schemas import AppointmentCreate, AppointmentResponse
from .services.booking_service import create_appointment, get_appointment_by_token, reschedule_appointment, delete_appointment
from .services.telegram_service import notify_user
from .services.ai_service import detect_specialization
from .services.doctor_service import get_doctors, get_availability
from pydantic import BaseModel
from datetime import datetime

Base.metadata.create_all(bind=engine)

from fastapi.staticfiles import StaticFiles
from .services.pdf_service import generate_receipt

# ... existing imports

app = FastAPI()

# Mount static files for PDFs
app.mount("/static", StaticFiles(directory="backend/static"), name="static")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class AIRequest(BaseModel):
    text: str

class SlotRequest(BaseModel):
    doctor_id: str
    date: str
    time: str
    telegram_id: int = None

def get_base_url():
    # Ideally from env, hardcoded for localhost now
    return "http://127.0.0.1:8000"

@app.post("/api/appointments", response_model=AppointmentResponse)
def book(payload: AppointmentCreate, db: Session = Depends(get_db)):
    appt = create_appointment(db, payload)
    notify_user(payload.phone, appt)
    
    # Generate Real PDF
    pdf_filename = generate_receipt(appt)
    pdf_url = f"{get_base_url()}/static/pdfs/{pdf_filename}"
    
    return {"token": appt.token, "status": appt.status, "pdf_url": pdf_url}

# ... (AI, Doctors, Availability endpoints unchanged)

@app.get("/appointments/{token}")
def get_booking(token: str, db: Session = Depends(get_db)):
    appt = get_appointment_by_token(db, token)
    if not appt:
        return {"error": "Not found"}
    
    # Generate PDF on the fly if needed, or check existence. 
    # For simplicity, regenerate or look it up. We'll regenerate to be safe.
    pdf_filename = generate_receipt(appt)
    pdf_url = f"{get_base_url()}/static/pdfs/{pdf_filename}"
    
    return {
        "doctor": appt.doctor,
        "date": appt.appointment_datetime.strftime("%Y-%m-%d"),
        "time": appt.appointment_datetime.strftime("%H:%M"),
        "service": appt.service,
        "pdf_url": pdf_url
    }

@app.post("/appointments")
def book_via_bot(payload: SlotRequest, db: Session = Depends(get_db)):
    # Convert date+time to datetime
    dt_str = f"{payload.date} {payload.time}"
    dt = datetime.strptime(dt_str, "%Y-%m-%d %H:%M")
    
    # Resolve doctor name
    doctors = get_doctors()
    doctor_obj = next((d for d in doctors if d["id"] == payload.doctor_id), None)
    doctor_name = doctor_obj["name"] if doctor_obj else f"Doctor {payload.doctor_id}"

    # We need a proper object for create_appointment
    class MockData:
        patient_name = "Telegram User"
        phone = str(payload.telegram_id)
        service = "Consultation"
        doctor = doctor_name
        appointment_datetime = dt
    
    appt = create_appointment(db, MockData())
    notify_user(MockData.phone, appt)
    
    # Generate Real PDF
    pdf_filename = generate_receipt(appt)
    pdf_url = f"{get_base_url()}/static/pdfs/{pdf_filename}"
    
    return {
        "date": appt.appointment_datetime.strftime("%Y-%m-%d"),
        "time": appt.appointment_datetime.strftime("%H:%M"),
        "doctor": appt.doctor,
        "calendar_link": f"https://calendar.google.com/calendar/render?action=TEMPLATE&text=Doctor+Appointment&dates={dt.strftime('%Y%m%dT%H%M%S')}/{dt.strftime('%Y%m%dT%H%M%S')}",
        "pdf_url": pdf_url
    }

@app.post("/ai/specialization")
def get_specialization(payload: AIRequest):
    return {"specialization": detect_specialization(payload.text)}

@app.get("/doctors")
def api_get_doctors(specialization: str = None):
    return get_doctors(specialization)

@app.get("/availability")
def api_get_availability(doctor_id: str, date: str):
    return get_availability(doctor_id, date)


@app.delete("/appointments/{token}")
def cancel_booking(token: str, db: Session = Depends(get_db)):
    success = delete_appointment(db, token)
    return {"success": success}
