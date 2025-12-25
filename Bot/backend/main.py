from fastapi import FastAPI
from backend.routes.booking_routes import router as booking_router

app = FastAPI(title="Hospital Booking Backend")

app.include_router(booking_router)

@app.get("/")
def health_check():
    return {"status": "Backend running"}
