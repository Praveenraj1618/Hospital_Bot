def detect_specialization(text: str) -> str:
    text = text.lower()
    if "heart" in text or "cardio" in text or "chest" in text:
        return "Cardiology"
    elif "skin" in text or "rash" in text or "derma" in text:
        return "Dermatology"
    elif "child" in text or "baby" in text or "pediatric" in text:
        return "Pediatrics"
    elif "bone" in text or "joint" in text or "fracture" in text:
        return "Orthopedics"
    elif "brain" in text or "headache" in text or "neuro" in text:
        return "Neurology"
    else:
        return "General Check-up"
