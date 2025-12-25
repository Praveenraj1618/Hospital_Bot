import requests
import json
from datetime import datetime

url = "http://127.0.0.1:8000/api/appointments"
payload = {
    "patient_name": "Test User",
    "phone": "9999999999",
    "service": "General Check-up",
    "doctor": "Dr. Smith",
    "appointment_datetime": datetime.now().isoformat()
}

try:
    response = requests.post(url, json=payload)
    print(f"Status Code: {response.status_code}")
    print(f"Response: {response.json()}")
except Exception as e:
    print(f"Error: {e}")
