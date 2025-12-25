from datetime import time

DOCTORS = {
    "Cardiology": [
        {
            "id": "cardio_1",
            "name": "Dr. Meera Shah",
            "experience": "8 years",
            "hospital": "Saroj Heart Clinic",
            "consultation_fee": 600,
        },
        {
            "id": "cardio_2",
            "name": "Dr. Anil Rao",
            "experience": "15 years",
            "hospital": "City Heart Institute",
            "consultation_fee": 900,
        }
    ],
    "Dermatology": [
         {
            "id": "derma_1",
            "name": "Dr. Priya Deshmukh",
            "experience": "6 years",
            "hospital": "Skin & Glow Clinic",
            "consultation_fee": 500,
        },
        {
             "id": "derma_2",
             "name": "Dr. Rajesh Gupta",
             "experience": "12 years",
             "hospital": "Clear Skin Centre",
             "consultation_fee": 700,
        }
    ],
    "General Medicine": [
        {
            "id": "gm_1",
            "name": "Dr. Ravi Kumar",
            "experience": "12 years",
            "hospital": "Saroj Multispeciality",
            "consultation_fee": 500,
        },
        {
            "id": "gm_2",
            "name": "Dr. Sangeeta Verma",
            "experience": "20 years",
            "hospital": "Community Health Center",
            "consultation_fee": 300,
        }
    ],
    "Pediatrics": [
        {
            "id": "ped_1",
            "name": "Dr. Arjun Singh",
            "experience": "5 years",
            "hospital": "Little Steps Clinic",
            "consultation_fee": 600,
        },
        {
            "id": "ped_2",
            "name": "Dr. Neha Kapoor",
            "experience": "10 years",
            "hospital": "City Children Hospital",
            "consultation_fee": 800,
        }
    ],
    "Orthopedics": [
        {
            "id": "ortho_1",
            "name": "Dr. Vikram Malhotra",
            "experience": "18 years",
            "hospital": "Bone & Joint Care",
            "consultation_fee": 1000,
        },
         {
            "id": "ortho_2",
            "name": "Dr. Sneha Patil",
            "experience": "9 years",
            "hospital": "Ortho Plus Clinic",
            "consultation_fee": 700,
        }
    ]
}

def get_doctors_by_specialization(specialization: str):
    return DOCTORS.get(specialization, [])
