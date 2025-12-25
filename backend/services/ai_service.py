import os
import logging
from groq import Groq
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

GROQ_API_KEY = os.getenv("GROQ_API_KEY")

# Client will be initialized only if key is present to avoid errors on import if missing
client = None
if GROQ_API_KEY:
    client = Groq(api_key=GROQ_API_KEY)
else:
    logging.warning("GROQ_API_KEY not found. AI features may not work.")

ALLOWED_SPECIALIZATIONS = [
    "Cardiology",
    "Orthopedics",
    "Dermatology",
    "Neurology",
    "General Medicine",
    "ENT",
    "Pediatrics",
    "Gynecology"
]

def extract_specialization(user_text: str) -> str:
    if not client:
        # Fallback if no API key
        return "General Medicine"

    prompt = f"""
Map the patient's issue to ONE specialization from this list:
{ALLOWED_SPECIALIZATIONS}

Patient says:
"{user_text}"

Reply with ONLY the specialization name.
If unsure, reply with "General Medicine".
"""

    try:
        response = client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=[
                {"role": "system", "content": "You are a medical intake assistant."},
                {"role": "user", "content": prompt}
            ],
            temperature=0
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        logging.error(f"Error in extract_specialization: {e}")
        return "General Medicine"
