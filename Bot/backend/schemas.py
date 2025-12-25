from pydantic import BaseModel
from datetime import datetime

class AppointmentCreate(BaseModel):
    hospital_id: int
    doctor_id: int
    patient_name: str
    patient_phone: str
    appointment_datetime: datetime
    source: str  # website / telegram / whatsapp


class AppointmentResponse(BaseModel):
    id: int
    token: str
    status: str

    class Config:
        orm_mode = True
