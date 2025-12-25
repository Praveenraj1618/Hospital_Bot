import os
from dotenv import load_dotenv
from groq import Groq

# Explicitly load .env from project root
load_dotenv(dotenv_path="../.env")

GROQ_API_KEY = os.getenv("GROQ_API_KEY")

if not GROQ_API_KEY:
    raise RuntimeError("GROQ_API_KEY not found. Check .env file location.")

client = Groq(api_key=GROQ_API_KEY)

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
    prompt = f"""
Map the patient's issue to ONE specialization from this list:
{ALLOWED_SPECIALIZATIONS}

Patient says:
"{user_text}"

Reply with ONLY the specialization name.
If unsure, reply with "General Medicine".
"""

    response = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[
            {"role": "system", "content": "You are a medical intake assistant."},
            {"role": "user", "content": prompt}
        ],
        temperature=0
    )

    return response.choices[0].message.content.strip()
