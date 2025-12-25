import urllib.parse
from datetime import datetime, timedelta

def generate_calendar_link(doctor, appointment_date, slot_time):
    start = datetime.combine(appointment_date, slot_time)
    end = start + timedelta(minutes=30)

    # Format dates as YYYYMMDDTHHMMSSZ (UTC) or local time if no Z. 
    # Google Calendar render link often expects YYYYMMDDTHHMMSS without separators if we want simple behavior,
    # but the user provided specific format: %Y%m%dT%H%M%S
    
    params = {
        "action": "TEMPLATE",
        "text": f"Doctor Appointment – {doctor['name']}",
        "dates": f"{start.strftime('%Y%m%dT%H%M%S')}/{end.strftime('%Y%m%dT%H%M%S')}",
        "details": f"Consultation at {doctor['hospital']}. Fee: ₹{doctor['consultation_fee']}",
        "location": doctor["hospital"],
        "trp": "false"
    }

    base_url = "https://calendar.google.com/calendar/render"
    return f"{base_url}?{urllib.parse.urlencode(params)}"
