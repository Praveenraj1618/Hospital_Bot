from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
import os
from datetime import datetime

PDF_DIR = "backend/static/pdfs"

if not os.path.exists(PDF_DIR):
    os.makedirs(PDF_DIR)

def generate_receipt(appointment):
    filename = f"receipt_{appointment.token}.pdf"
    filepath = os.path.join(PDF_DIR, filename)
    
    c = canvas.Canvas(filepath, pagesize=letter)
    width, height = letter
    
    # Header
    c.setFont("Helvetica-Bold", 24)
    c.drawString(50, height - 50, "ProHealth Hospital")
    
    c.setFont("Helvetica", 12)
    c.drawString(50, height - 80, "Appointment Receipt")
    
    # Details
    c.line(50, height - 90, width - 50, height - 90)
    
    y = height - 120
    line_height = 25
    
    details = [
        f"Token: {appointment.token}",
        f"Date: {appointment.appointment_datetime.strftime('%Y-%m-%d')}",
        f"Time: {appointment.appointment_datetime.strftime('%H:%M')}",
        f"Doctor: {appointment.doctor}",
        f"Service: {appointment.service}",
        f"Patient: {appointment.patient_name}",
        f"Phone: {appointment.phone}",
        f"Status: {appointment.status}"
    ]
    
    for detail in details:
        c.drawString(50, y, detail)
        y -= line_height
        
    # Footer
    c.line(50, y - 10, width - 50, y - 10)
    c.drawString(50, y - 30, "Please arrive 15 minutes before your scheduled time.")
    c.drawString(50, y - 45, "For support, contact care@prohealth.com")
    
    c.save()
    return filename
