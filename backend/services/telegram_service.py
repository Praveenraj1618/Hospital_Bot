from telegram import Bot
import os

# Ideally load this from environment variables
BOT_TOKEN = os.getenv("BOT_TOKEN")
# Replace with your actual bot username if known, or load from env
BOT_USERNAME = os.getenv("BOT_USERNAME", "TheMedixBot")
BOT_CHAT_LINK = f"https://t.me/{BOT_USERNAME}"

# Initialize bot only if token is present to avoid errors on startup if not executing
if BOT_TOKEN:
    bot = Bot(token=BOT_TOKEN)
else:
    bot = None

def notify_user(phone, appointment):
    message = (
        f"✅ Appointment Confirmed\n\n"
        f"👤 {appointment.patient_name}\n"
        f"🩺 {appointment.service}\n"
        f"👨‍⚕️ {appointment.doctor}\n"
        f"📅 {appointment.appointment_datetime}\n"
        f"🎫 Token: {appointment.token}\n\n"
        f"For reschedule, cancel, reminders and support,\n"
        f"continue here 👉 {BOT_CHAT_LINK}"
    )

    # Later: map phone -> chat_id real message sending logic
    print("[BOT MESSAGE]")
    print(message)
