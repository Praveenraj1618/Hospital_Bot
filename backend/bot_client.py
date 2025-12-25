import requests
import os

API_URL = "http://127.0.0.1:8000/api/appointments"

def get_appointment_by_token(token):
    try:
        r = requests.get(f"{API_URL}/{token}")
        if r.status_code != 200:
            return None
        return r.json()
    except Exception as e:
        print(f"Error fetching appointment: {e}")
        return None

def cancel_appointment_api(token):
    try:
        r = requests.delete(f"{API_URL}/{token}")
        return r.status_code == 200
    except Exception as e:
        print(f"Error cancelling appointment: {e}")
        return False

def reschedule_appointment(token, new_datetime):
    try:
        r = requests.patch(
            f"{API_URL}/{token}/reschedule",
            params={"new_datetime": new_datetime}
        )
        return r.status_code == 200
    except Exception as e:
        print(f"Error rescheduling: {e}")
        return False
