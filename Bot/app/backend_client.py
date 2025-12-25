import httpx

BACKEND_URL = "http://127.0.0.1:8000"

def book_appointment(payload):
    # Using a timeout to prevent hanging
    try:
        response = httpx.post(
            f"{BACKEND_URL}/appointments/book",
            json=payload,
            timeout=10
        )

        if response.status_code == 409:
            return {"error": "Slot already booked"}
        
        # Raise error for other non-200 codes
        response.raise_for_status()
        return response.json()
    except httpx.RequestError as e:
        print(f"An error occurred while requesting {e.request.url!r}.")
        return {"error": "Backend connection failed"}
    except httpx.HTTPStatusError as e:
        print(f"Error response {e.response.status_code} while requesting {e.request.url!r}.")
        return {"error": f"Server error: {e.response.status_code}"}
