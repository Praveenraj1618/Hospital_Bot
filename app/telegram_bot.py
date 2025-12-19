import asyncio
import os
import sys
import calendar
from doctors import DOCTORS
from appointments import APPOINTMENTS
from calendar_sync import add_to_calendar
from reminders import schedule_reminders
from calendar_links import generate_calendar_link
from datetime import datetime, timedelta, date, time
import random
from telegram import InlineKeyboardButton, InlineKeyboardMarkup

# Windows asyncio fix
if sys.platform.startswith("win"):
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

from telegram import Update
from telegram.request import HTTPXRequest
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    MessageHandler,
    CallbackQueryHandler,
    ContextTypes,
    filters
)

from ai import extract_specialization
import os
BOT_TOKEN = os.getenv("BOT_TOKEN")


GREETINGS = {"hi", "hello", "hey", "heyy", "hii","hiii", "hiiii","hiiiii", "hola"}
THANKS = {"thanks", "thank you", "thx"}
GOODBYES = {"bye", "goodbye", "see you", "exit"}

START_MESSAGES = [
    "👋 Hi! What health concern can I help you with today?",
    "Hello 🙂 Please tell me your reason for visiting.",
    "Hi there! What seems to be the issue?",
    "👋 Welcome! Tell me your health concern to get started."
]

def normalize(text: str):
    return text.lower().strip()


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data.clear()
    await update.message.reply_text(
        "👋 Hi! Please tell me your health concern or reason for visit."
    )


async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_text = update.message.text
    text = normalize(user_text)

    # 1️⃣ Greetings → restart flow
    if text in GREETINGS:
        context.user_data.clear()
        await update.message.reply_text(random.choice(START_MESSAGES))
        return

    # 2️⃣ Thanks
    if text in THANKS:
        await update.message.reply_text("😊 You’re welcome!")
        return

    # 3️⃣ Goodbye
    if text in GOODBYES:
        context.user_data.clear()
        await update.message.reply_text(
            "👋 Take care! Feel free to come back anytime."
        )
        return

    if text == "yes" and "doctor_id" in context.user_data:
        await show_calendar(update, context)
        return

    if text == "back" and "specialization" in context.user_data:
        # re-show doctor list
        specialization = context.user_data["specialization"]
        doctors = DOCTORS.get(specialization, [])

        if not doctors:
             await update.message.reply_text(
                f"No doctors found for {specialization}."
            )
             return

        keyboard = []
        for doc in doctors:
            button_text = (
                f"{doc['name']} | {doc['experience']} | ₹{doc['consultation_fee']}"
            )
            keyboard.append([
                InlineKeyboardButton(button_text, callback_data=doc["id"])
            ])

        reply_markup = InlineKeyboardMarkup(keyboard)
        await update.message.reply_text(
            f"Based on your concern, please choose a {specialization} specialist:",
            reply_markup=reply_markup
        )
        return

    await update.message.reply_text("🔍 Understanding your concern...")

    try:
        # 1️⃣ AI → specialization
        specialization = extract_specialization(user_text)
        context.user_data["specialization"] = specialization

        doctors = DOCTORS.get(specialization, [])

        if not doctors:
            await update.message.reply_text(
                f"No doctors found for {specialization}."
            )
            return

        # 2️⃣ Build inline buttons
        keyboard = []
        for doc in doctors:
            button_text = (
                f"{doc['name']} | {doc['experience']} | ₹{doc['consultation_fee']}"
            )
            keyboard.append([
                InlineKeyboardButton(button_text, callback_data=doc["id"])
            ])

        reply_markup = InlineKeyboardMarkup(keyboard)

        # 3️⃣ Show doctors
        await update.message.reply_text(
            f"Based on your concern, please choose a {specialization} specialist:",
            reply_markup=reply_markup
        )

    except Exception as e:
        print("ERROR:", e)
        await update.message.reply_text(
            "⚠️ Sorry, I couldn't process that right now. Please try again."
        )


async def handle_doctor_selection(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    doctor_id = query.data
    specialization = context.user_data.get("specialization")

    # Find selected doctor
    doctor = next(
        (d for d in DOCTORS.get(specialization, []) if d["id"] == doctor_id),
        None
    )

    if not doctor:
        await query.edit_message_text("⚠️ Doctor not found.")
        return

    context.user_data["doctor_id"] = doctor_id

    doctor_profile = (
        f"👨‍⚕️ *{doctor['name']}*\n\n"
        f"🏥 Hospital: {doctor['hospital']}\n"
        f"🎓 Qualification: {doctor['qualification']}\n"
        f"⏳ Experience: {doctor['experience']}\n"
        f"💬 Languages: {doctor['languages']}\n"
        f"💰 Consultation Fee: ₹{doctor['consultation_fee']}\n\n"
        f"🩺 About:\n{doctor['about']}\n\n"
        f"✅ Reply *YES* to book an appointment with this doctor\n"
        f"🔙 Or type *BACK* to choose another doctor"
    )

    await query.edit_message_text(
        doctor_profile,
        parse_mode="Markdown"
    )


def get_selected_doctor(context):
    specialization = context.user_data.get("specialization")
    doctor_id = context.user_data.get("doctor_id")

    if not specialization or not doctor_id:
        return None

    return next(
        (d for d in DOCTORS.get(specialization, []) if d["id"] == doctor_id),
        None
    )



def has_availability(doctor, selected_date):
    slots = generate_slots(doctor, selected_date)
    return len(slots) > 0


def build_calendar(doctor, year, month):
    cal = calendar.Calendar()
    today = date.today()

    keyboard = []

    # Header row (Month Year)
    keyboard.append([
        InlineKeyboardButton(
            f"{calendar.month_name[month]} {year}",
            callback_data="ignore"
        )
    ])

    # Weekday headers
    keyboard.append([
        InlineKeyboardButton(d, callback_data="ignore")
        for d in ["Mo", "Tu", "We", "Th", "Fr", "Sa", "Su"]
    ])

    week = []
    for day in cal.itermonthdates(year, month):
        if day.month != month or day < today:
            # Empty / past dates
            week.append(InlineKeyboardButton(" ", callback_data="ignore"))
        else:
            if has_availability(doctor, day):
                # Available date
                week.append(
                    InlineKeyboardButton(
                        f"🟢{day.day}",
                        callback_data=f"date_{day.isoformat()}"
                    )
                )
            else:
                # No slots
                week.append(
                    InlineKeyboardButton(
                        f"🔴{day.day}",
                        callback_data="ignore"
                    )
                )

        if len(week) == 7:
            keyboard.append(week)
            week = []

    if week:
        keyboard.append(week)

    # Navigation buttons
    prev_month = month - 1 if month > 1 else 12
    prev_year = year if month > 1 else year - 1

    next_month = month + 1 if month < 12 else 1
    next_year = year if month < 12 else year + 1

    keyboard.append([
        InlineKeyboardButton("⬅️", callback_data=f"cal_{prev_year}_{prev_month}"),
        InlineKeyboardButton("➡️", callback_data=f"cal_{next_year}_{next_month}")
    ])

    return InlineKeyboardMarkup(keyboard)


async def show_calendar(update, context):
    doctor = get_selected_doctor(context)
    today = date.today()

    # Default to current month if not set
    year = context.user_data.get("calendar_year", today.year)
    month = context.user_data.get("calendar_month", today.month)

    # Update context
    context.user_data["calendar_year"] = year
    context.user_data["calendar_month"] = month

    reply_markup = build_calendar(doctor, year, month)

    target = update.message if update.message else update.callback_query.message
    
    # If called from a callback, we want to edit or reply? 
    # Usually show_calendar is called from 'yes' message, so reply_text is fine.
    # But for navigation we need edit. Let's make it flexible or handle navigation separately.
    # For now, show_calendar is only used for initial display. Navigation uses handle_calendar_navigation.
    
    await target.reply_text(
        "📅 Select an available date:",
        reply_markup=reply_markup
    )


async def handle_calendar_navigation(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    _, year, month = query.data.split("_")
    year, month = int(year), int(month)

    context.user_data["calendar_year"] = year
    context.user_data["calendar_month"] = month

    doctor = get_selected_doctor(context)

    await query.edit_message_reply_markup(
        reply_markup=build_calendar(doctor, year, month)
    )


def generate_slots(doctor, selected_date):
    opd = doctor["opd"]
    slots = []

    # Combine date with opd times
    start_dt = datetime.combine(selected_date, opd["start"])
    end_dt = datetime.combine(selected_date, opd["end"])
    now = datetime.now()

    while start_dt < end_dt:
        # Check if slot is in the past (for today)
        if start_dt > now:
            slot_time = start_dt.time()

            # Check availability
            is_booked = any(
                a["doctor_id"] == doctor["id"] and
                a["date"] == selected_date and
                a["time"] == slot_time
                for a in APPOINTMENTS
            )

            if not is_booked:
                slots.append(slot_time)

        start_dt += timedelta(minutes=opd["slot_minutes"])

    return slots


async def handle_ignore(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    # Do nothing else


async def handle_date_selection(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    date_str = query.data.replace("date_", "")
    selected_date = date.fromisoformat(date_str)
    context.user_data["date"] = selected_date

    doctor = get_selected_doctor(context)
    if not doctor:
        await query.edit_message_text("⚠️ Session expired. Please start over.")
        return

    slots = generate_slots(doctor, selected_date)

    if not slots:
        await query.edit_message_text(
            f"❌ No slots available on {selected_date.strftime('%d %b')}.\nPlease go back and choose another date."
        )
        return

    keyboard = []
    # 2 slots per row
    row = []
    for s in slots:
        row.append(InlineKeyboardButton(s.strftime("%I:%M %p"), callback_data=f"slot_{s}"))
        if len(row) == 2:
            keyboard.append(row)
            row = []
    if row:
        keyboard.append(row)

    await query.edit_message_text(
        f"🗓 *{selected_date.strftime('%a, %d %b')}*\n⏰ Select a time slot:",
        reply_markup=InlineKeyboardMarkup(keyboard),
        parse_mode="Markdown"
    )


async def handle_slot_selection(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    slot_time_str = query.data.replace("slot_", "")
    # Parse string back to time object (assuming HH:MM:SS from str(time))
    try:
        slot_time = datetime.strptime(slot_time_str, "%H:%M:%S").time()
    except ValueError:
        slot_time = datetime.strptime(slot_time_str, "%H:%M").time()

    context.user_data["time"] = slot_time

    doctor = get_selected_doctor(context)
    appointment_date = context.user_data["date"]

    # Save to store
    APPOINTMENTS.append({
        "doctor_id": doctor["id"],
        "date": appointment_date,
        "time": slot_time
    })

    token = f"HSP-{random.randint(10000, 99999)}"

    # Sync to Google Calendar
    add_to_calendar(doctor, appointment_date, slot_time)

    # Schedule reminders
    # Need to reconstruct the appointment dict exactly as expected by scheduler
    appointment_full = {
        "doctor_id": doctor["id"],
        "date": appointment_date,
        "time": slot_time,
        "datetime": datetime.combine(appointment_date, slot_time),
        "chat_id": query.message.chat_id
    }
    # Update global store with full object (conceptually replacing the simpler one added above)
    # Actually, let's just update the last entry or append the full one correctly first.
    APPOINTMENTS.pop()
    APPOINTMENTS.append(appointment_full)
    
    schedule_reminders(context.bot, appointment_full)

    # Generate Calendar Link
    calendar_link = generate_calendar_link(doctor, appointment_date, slot_time)

    await query.edit_message_text(
        f"✅ *Appointment Confirmed*\n\n"
        f"👨‍⚕️ *{doctor['name']}*\n"
        f"🏥 {doctor['hospital']}\n"
        f"📅 {appointment_date.strftime('%A, %d %b %Y')}\n"
        f"⏰ {slot_time.strftime('%I:%M %p')}\n"
        f"💰 Fee: ₹{doctor['consultation_fee']}\n"
        f"🎫 Token: `{token}`\n\n"
        f"Thank you for using Hospital Bot! 👋\n\n"
        f"📅 *Add to your calendar*\n{calendar_link}",
        parse_mode="Markdown"
    )


async def error_handler(update, context):
    print("Unhandled error:", context.error)


def main():
    request = HTTPXRequest(connect_timeout=60, read_timeout=60)
    app = ApplicationBuilder().token(BOT_TOKEN).request(request).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    app.add_handler(CallbackQueryHandler(handle_doctor_selection, pattern="^(cardio|gm|ped|derma|ortho)_"))
    app.add_handler(CallbackQueryHandler(handle_calendar_navigation, pattern="^cal_"))
    app.add_handler(CallbackQueryHandler(handle_date_selection, pattern="^date_"))
    app.add_handler(CallbackQueryHandler(handle_ignore, pattern="^ignore$"))
    app.add_handler(CallbackQueryHandler(handle_slot_selection, pattern="^slot_"))
    app.add_error_handler(error_handler)

    print("Bot is running with AI + Doctor selection...")
    app.run_polling()


if __name__ == "__main__":
    main()
