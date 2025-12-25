from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from backend.database import get_db
from backend.schemas import AppointmentCreate, AppointmentResponse
from backend.services.booking_service import create_appointment

router = APIRouter(prefix="/appointments", tags=["Appointments"])

@router.post("/book", response_model=AppointmentResponse)
def book_appointment(
    payload: AppointmentCreate,
    db: Session = Depends(get_db)
):
    try:
        appt = create_appointment(db, payload)
        return appt
    except ValueError as e:
        raise HTTPException(status_code=409, detail=str(e))
