from pydantic import BaseModel
from datetime import datetime

class AppointmentCreate(BaseModel):
    patient_name: str
    phone: str
    service: str
    doctor: str
    appointment_datetime: datetime

class AppointmentResponse(BaseModel):
    token: str
    status: str

class AppointmentDetail(BaseModel):
    patient_name: str
    service: str
    doctor: str
    appointment_datetime: datetime
    token: str
    status: str
