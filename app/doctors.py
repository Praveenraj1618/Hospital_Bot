from datetime import time

DOCTORS = {
    "Cardiology": [
        {
            "id": "cardio_1",
            "name": "Dr. Meera Shah",
            "experience": "8 years",
            "qualification": "MBBS, MD (Cardiology)",
            "hospital": "Saroj Heart Clinic",
            "consultation_fee": 600,
            "languages": "English, Tamil",
            "about": "Specializes in preventive cardiology and lifestyle disorders.",
            "opd": {
                "start": time(10, 0),
                "end": time(14, 0),
                "slot_minutes": 30
            }
        },
        {
            "id": "cardio_2",
            "name": "Dr. Anil Rao",
            "experience": "15 years",
            "qualification": "MBBS, DM (Cardiology)",
            "hospital": "City Heart Institute",
            "consultation_fee": 900,
            "languages": "English, Hindi",
            "about": "Expert in interventional cardiology and cardiac procedures.",
            "opd": {
                "start": time(16, 0),
                "end": time(20, 0),
                "slot_minutes": 45
            }
        }
    ],
    "Dermatology": [
         {
            "id": "derma_1",
            "name": "Dr. Priya Deshmukh",
            "experience": "6 years",
            "qualification": "MBBS, MD (Dermatology)",
            "hospital": "Skin & Glow Clinic",
            "consultation_fee": 500,
            "languages": "English, Marathi",
            "about": "Specialist in acne, scarring, and anti-aging treatments.",
            "opd": {
                "start": time(11, 0),
                "end": time(15, 0),
                "slot_minutes": 20
            }
        },
        {
             "id": "derma_2",
             "name": "Dr. Rajesh Gupta",
             "experience": "12 years",
             "qualification": "MBBS, DDVL",
             "hospital": "Clear Skin Centre",
             "consultation_fee": 700,
             "languages": "Hindi, English",
             "about": "Focuses on hair transplant and laser treatments.",
             "opd": {
                 "start": time(17, 0),
                 "end": time(21, 0),
                 "slot_minutes": 30
             }
        }
    ],
    "General Medicine": [
        {
            "id": "gm_1",
            "name": "Dr. Ravi Kumar",
            "experience": "12 years",
            "qualification": "MBBS, MD (General Medicine)",
            "hospital": "Saroj Multispeciality",
            "consultation_fee": 500,
            "languages": "English, Telugu",
            "about": "Treats common illnesses, fever, diabetes, and hypertension.",
            "opd": {
                "start": time(9, 0),
                "end": time(13, 0),
                "slot_minutes": 15
            }
        },
        {
            "id": "gm_2",
            "name": "Dr. Sangeeta Verma",
            "experience": "20 years",
            "qualification": "MBBS, DNB (Family Medicine)",
            "hospital": "Community Health Center",
            "consultation_fee": 300,
            "languages": "Hindi, Punjabi",
            "about": "Experienced family physician treating all age groups.",
            "opd": {
                "start": time(10, 0),
                "end": time(14, 0),
                "slot_minutes": 20
            }
        }
    ],
    "Pediatrics": [
        {
            "id": "ped_1",
            "name": "Dr. Arjun Singh",
            "experience": "5 years",
            "qualification": "MBBS, MD (Pediatrics)",
            "hospital": "Little Steps Clinic",
            "consultation_fee": 600,
            "languages": "English, Hindi",
            "about": "Specialist in child vaccination and development.",
            "opd": {
                "start": time(16, 0),
                "end": time(19, 0),
                "slot_minutes": 20
            }
        },
        {
            "id": "ped_2",
            "name": "Dr. Neha Kapoor",
            "experience": "10 years",
            "qualification": "MBBS, DCH",
            "hospital": "City Children Hospital",
            "consultation_fee": 800,
            "languages": "English, Marathi",
            "about": "Expert in pediatric nutrition and infectious diseases.",
            "opd": {
                "start": time(9, 30),
                "end": time(12, 30),
                "slot_minutes": 15
            }
        }
    ],
    "Orthopedics": [
        {
            "id": "ortho_1",
            "name": "Dr. Vikram Malhotra",
            "experience": "18 years",
            "qualification": "MBBS, MS (Orthopedics)",
            "hospital": "Bone & Joint Care",
            "consultation_fee": 1000,
            "languages": "English, Hindi",
            "about": "Specializes in joint replacement and sports injuries.",
            "opd": {
                "start": time(10, 0),
                "end": time(13, 0),
                "slot_minutes": 30
            }
        },
         {
            "id": "ortho_2",
            "name": "Dr. Sneha Patil",
            "experience": "9 years",
            "qualification": "MBBS, D.Ortho",
            "hospital": "Ortho Plus Clinic",
            "consultation_fee": 700,
            "languages": "English, Kannda",
            "about": "Expert in fracture management and physiotherapy.",
            "opd": {
                "start": time(17, 30),
                "end": time(20, 30),
                "slot_minutes": 30
            }
        }
    ]
}
