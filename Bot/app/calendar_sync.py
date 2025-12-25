from googleapiclient.discovery import build
from google.oauth2.service_account import Credentials
from datetime import datetime, timedelta
import os
import json

# Define scopes
SCOPES = ["https://www.googleapis.com/auth/calendar"]

# Try to find credentials in current dir or parent dir
def get_calendar_service():
    creds_json = os.getenv("GOOGLE_CREDENTIALS_JSON")
    if not creds_json:
        print("Warning: GOOGLE_CREDENTIALS_JSON env var not found. Calendar sync will be skipped.")
        return None

    try:
        creds_info = json.loads(creds_json)
        creds = Credentials.from_service_account_info(creds_info, scopes=SCOPES)
        return build("calendar", "v3", credentials=creds)
    except Exception as e:
        print(f"Error loading credentials: {e}")
        return None

def add_to_calendar(doctor, appointment_date, slot_time):
    service = get_calendar_service()
    if not service:
        return

    try:
        start = datetime.combine(appointment_date, slot_time)
        end = start + timedelta(minutes=30)

        event = {
            "summary": f"Doctor Appointment – {doctor['name']}",
            "location": doctor["hospital"],
            "description": f"Consultation fee: ₹{doctor['consultation_fee']}",
            "start": {"dateTime": start.isoformat(), "timeZone": "Asia/Kolkata"},
            "end": {"dateTime": end.isoformat(), "timeZone": "Asia/Kolkata"},
            "reminders": {
                "useDefault": False,
                "overrides": [
                    {"method": "popup", "minutes": 60},
                    {"method": "popup", "minutes": 1440}
                ],
            },
        }

        service.events().insert(calendarId="5793397678d2192cda3b76adf26222eaf0af2e0dde609b6fc7be35e2cd9d9fda@group.calendar.google.com", body=event).execute()
        print(f"Event created for {doctor['name']} at {start}")
    except Exception as e:
        print(f"Failed to create calendar event: {e}")
