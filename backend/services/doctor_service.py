doctors_db = [
    # Cardiology
    {
        "id": "1", 
        "name": "Dr. Neha Kapoor", 
        "specialization": "Cardiology", 
        "experience": "12 years", 
        "qualification": "MBBS, MD (Cardiology), AIIMS",
        "languages": "English, Hindi",
        "fees": "₹1500",
        "about": "Senior Cardiologist specializing in interventional cardiology and heart failure management. Recipient of the 'Best Cardiologist' award 2023."
    },
    {
        "id": "7", 
        "name": "Dr. Arjun Reddy", 
        "specialization": "Cardiology", 
        "experience": "18 years", 
        "qualification": "MBBS, DM (Cardiology), FRCP (London)",
        "languages": "English, Telugu, Hindi",
        "fees": "₹2000",
        "about": "Expert in pediatric cardiology and complex heart surgeries. Over 5000 successful surgeries performed."
    },
    
    # Dermatology
    {
        "id": "2", 
        "name": "Dr. Amit Sharma", 
        "specialization": "Dermatology", 
        "experience": "8 years",
        "qualification": "MBBS, DVD, DNB",
        "languages": "English, Hindi, Punjabi",
        "fees": "₹1000",
        "about": "Focused on clinical dermatology, cosmetic procedures, and laser treatments for skin rejuvenation."
    },
    {
        "id": "8", 
        "name": "Dr. Kavita Mehra", 
        "specialization": "Dermatology", 
        "experience": "14 years",
        "qualification": "MBBS, MD (Dermatology)",
        "languages": "English, Hindi",
        "fees": "₹1200",
        "about": "Specialist in acne treatment, anti-aging therapies, and hair transplant surgeries."
    },

    # Pediatrics
    {
        "id": "3", 
        "name": "Dr. Priya Singh", 
        "specialization": "Pediatrics", 
        "experience": "15 years",
        "qualification": "MBBS, MD (Pediatrics)",
        "languages": "English, Hindi, Marathi",
        "fees": "₹800",
        "about": "Compassionate pediatrician with extensive experience in child vaccination, growth monitoring, and nutrition."
    },
    {
        "id": "9", 
        "name": "Dr. Rohan Das", 
        "specialization": "Pediatrics", 
        "experience": "10 years",
        "qualification": "MBBS, DCH",
        "languages": "English, Bengali, Hindi",
        "fees": "₹900",
        "about": "Friendly child specialist known for making kids feel comfortable. Expert in treating seasonal viral fevers."
    },

    # Orthopedics
    {
        "id": "4", 
        "name": "Dr. Rajesh Verma", 
        "specialization": "Orthopedics", 
        "experience": "20 years",
        "qualification": "MBBS, MS (Ortho)",
        "languages": "English, Hindi",
        "fees": "₹1800",
        "about": "Renowned Orthopedic Surgeon specializing in knee and hip replacement surgeries and sports injury rehabilitation."
    },
    {
        "id": "10", 
        "name": "Dr. Suresh Nair", 
        "specialization": "Orthopedics", 
        "experience": "12 years",
        "qualification": "MBBS, D.Ortho",
        "languages": "English, Malayalam, Hindi",
        "fees": "₹1400",
        "about": "Expert in spine surgery and minimally invasive orthopedic procedures."
    },

    # General Check-up / General Medicine
    {
        "id": "6", 
        "name": "Dr. Viking", 
        "specialization": "General Check-up", 
        "experience": "5 years",
        "qualification": "MBBS",
        "languages": "English",
        "fees": "₹500",
        "about": "Dedicated to preventive healthcare, general wellness, and lifestyle disease management."
    },
    {
        "id": "11", 
        "name": "Dr. Sarah Khan", 
        "specialization": "General Check-up", 
        "experience": "9 years",
        "qualification": "MBBS, MD (Internal Medicine)",
        "languages": "English, Urdu, Hindi",
        "fees": "₹700",
        "about": "Experienced physician managing diabetes, hypertension, and thyroid disorders."
    }
]

def get_doctors(specialization: str = None):
    # Mock search: if exact match fails, try partial match (case insensitive)
    if specialization:
        # Standardize spec to title case
        spec_title = specialization.title()
        
        # Exact match
        matches = [d for d in doctors_db if d["specialization"].lower() == specialization.lower()]
        
        # If no matches, try to find default "General Check-up" if input was generic
        if not matches and "general" in specialization.lower():
             return [d for d in doctors_db if "General" in d["specialization"]]
             
        return matches
        
    return doctors_db

def get_availability(doctor_id: str, date: str):
    # Mock availability
    return ["09:00", "09:30", "10:00", "11:00", "11:30", "14:00", "14:30", "16:00", "17:00"]
