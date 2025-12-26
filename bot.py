import os
import requests
import calendar
from datetime import datetime, timedelta
from telegram import (
    Update,
    InlineKeyboardButton,
    InlineKeyboardMarkup
)
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    MessageHandler,
    CallbackQueryHandler,
    ContextTypes,
    filters
)
from dotenv import load_dotenv

load_dotenv()

# ================= CONFIG =================
BOT_TOKEN = os.getenv("BOT_TOKEN") 
BACKEND_URL = "http://127.0.0.1:8000"

# ================= HELPERS =================

def api_get(path, params=None):
    try:
        response = requests.get(f"{BACKEND_URL}{path}", params=params)
        response.raise_for_status()
        return response.json()
    except Exception as e:
        print(f"API Error {path}: {e}")
        return {}

def api_post(path, payload):
    try:
        response = requests.post(f"{BACKEND_URL}{path}", json=payload)
        response.raise_for_status()
        return response.json()
    except Exception as e:
        print(f"API Error {path}: {e}")
        return {}

def api_delete(path):
    try:
        response = requests.delete(f"{BACKEND_URL}{path}")
        response.raise_for_status()
        return response.json()
    except Exception as e:
        print(f"API Error {path}: {e}")
        return {}

# ================= START =================

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data.clear()
    args = context.args

    # Website redirect with token
    if args and args[0].startswith("token_"):
        token = args[0].replace("token_", "")
        booking = api_get(f"/appointments/{token}")

        if "error" in booking or not booking:
            await update.message.reply_text("❌ Invalid booking token.")
            return

        context.user_data["mode"] = "post_booking"
        context.user_data["token"] = token

        # Send PDF if available
        pdf_url = booking.get("pdf_url")
        if pdf_url:
            await update.message.reply_text(f"📄 Booking Receipt: {pdf_url}")

        await show_post_booking_menu(update)
        return

    # Normal entry
    context.user_data["mode"] = "idle"

    keyboard = [
        [InlineKeyboardButton("📅 Book Appointment", callback_data="menu_book")],
        [InlineKeyboardButton("📞 Contact Hospital", callback_data="menu_contact")]
    ]

    await update.message.reply_text(
        "👋 Welcome to *ProHealth Hospital Assistant*\n\nHow can I help you?",
        parse_mode="Markdown",
        reply_markup=InlineKeyboardMarkup(keyboard)
    )

# ================= MENUS =================

async def show_post_booking_menu(update):
    keyboard = [
        [InlineKeyboardButton("📄 Show Details", callback_data="pb_details")],
        [InlineKeyboardButton("🔄 Reschedule", callback_data="pb_reschedule")],
        [InlineKeyboardButton("❌ Cancel Appointment", callback_data="pb_cancel")]
    ]
    
    # Check if called from message or callback
    if update.callback_query:
        await update.callback_query.edit_message_text(
            "What would you like to do next?",
            reply_markup=InlineKeyboardMarkup(keyboard)
        )
    else:
        await update.message.reply_text(
            "What would you like to do next?",
            reply_markup=InlineKeyboardMarkup(keyboard)
        )

# ================= CALLBACK HANDLERS =================

async def handle_menu(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    if query.data == "menu_book":
        context.user_data.clear()
        context.user_data["mode"] = "booking"
        await query.edit_message_text(
            "🩺 Please tell me your health concern or reason for visit."
        )

    elif query.data == "menu_contact":
        await query.edit_message_text(
            "📞 You can contact us at:\n\n☎ +91-XXXXXXXXXX\n📧 care@prohealth.com"
        )

# ================= BOOKING FLOW =================

async def handle_text(update: Update, context: ContextTypes.DEFAULT_TYPE):
    mode = context.user_data.get("mode")
    text = update.message.text.strip()

    if mode == "booking":
        await detect_specialization(update, context, text)
        return

    await update.message.reply_text(
        "Please use the menu or type *Hi* to start again.",
        parse_mode="Markdown"
    )

async def detect_specialization(update, context, text):
    msg = await update.message.reply_text("🔍 Understanding your concern...")

    res = api_post("/ai/specialization", {"text": text})
    specialization = res.get("specialization", "General Check-up")
    context.user_data["specialization"] = specialization

    await show_doctor_list(update, context, specialization, msg)

async def show_doctor_list(update, context, specialization, message_obj=None):
    doctors = api_get("/doctors", {"specialization": specialization})
    
    if not doctors:
        text = f"No doctors found for {specialization}."
        if message_obj:
            await message_obj.edit_text(text)
        else:
            await update.callback_query.edit_message_text(text)
        return

    # Show doctor name + experience in button
    keyboard = [
        [InlineKeyboardButton(f"{d['name']} ({d['experience']})", callback_data=f"doc_{d['id']}")]
        for d in doctors
    ]

    text = f"🩺 *{specialization}* specialists available:\nSelect a doctor to view profile."
    
    if message_obj:
        await message_obj.edit_text(text, parse_mode="Markdown", reply_markup=InlineKeyboardMarkup(keyboard))
    else:
        # Called from 'Back' button
        await update.callback_query.edit_message_text(text, parse_mode="Markdown", reply_markup=InlineKeyboardMarkup(keyboard))

async def handle_doctor(update, context):
    query = update.callback_query
    await query.answer()

    doctor_id = query.data.replace("doc_", "")
    context.user_data["doctor_id"] = doctor_id
    
    # Fetch doctor details
    specialization = context.user_data.get("specialization")
    doctors = api_get("/doctors", {"specialization": specialization})
    # If we are in reschedule mode or context lost, fetch all to be safe
    if not doctors: 
        doctors = api_get("/doctors")
        
    doctor = next((d for d in doctors if d["id"] == doctor_id), None)

    if not doctor:
        await query.edit_message_text("Doctor not found.")
        return

    # Enhanced Portfolio View
    text = (
        f"👨‍⚕️ *{doctor['name']}*\n"
        f"🩺 *{doctor['specialization']}*\n\n"
        f"🎓 {doctor.get('qualification', 'MBBS')}\n"
        f"💼 Exp: {doctor['experience']}  |  💰 Fees: {doctor.get('fees', 'N/A')}\n"
        f"🗣 {doctor.get('languages', 'English')}\n\n"
        f"📝 *About:*\n{doctor['about']}\n"
    )

    keyboard = [
        [InlineKeyboardButton("📅 Book Appointment", callback_data="start_book")],
        [InlineKeyboardButton("🔙 Back to List", callback_data="back_docs")]
    ]

    await query.edit_message_text(text, parse_mode="Markdown", reply_markup=InlineKeyboardMarkup(keyboard))

async def handle_back_to_doctors(update, context):
    query = update.callback_query
    await query.answer()
    specialization = context.user_data.get("specialization")
    if not specialization:
        # Fallback: if we can't remember spec, send them to menu or generic list
        # Best user exp: Ask them to start over or show all categories. 
        # For now, let's show General docs or ask to pick spec logic again? 
        # Simpler:
        await query.edit_message_text("Session expired. Please start booking again.", 
                                      reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("Start Over", callback_data="menu_book")]]))
        return
        
    await show_doctor_list(update, context, specialization)

# ... (rest of calendar/date handlers remain) 

# ...

# ================= POST BOOKING =================

async def handle_post_booking(update, context):
    query = update.callback_query
    await query.answer()
    token = context.user_data["token"]

    if query.data == "pb_details":
        booking = api_get(f"/appointments/{token}")
        pdf_url = booking.get("pdf_url", "")
        
        text = (
            f"📄 *Appointment Details*\n\n"
            f"👨‍⚕️ {booking['doctor']}\n"
            f"📅 {booking['date']} {booking['time']}\n"
            f"📥 [Download Receipt]({pdf_url})"
        )
        await query.edit_message_text(text, parse_mode="Markdown")

    elif query.data == "pb_reschedule":
        context.user_data["mode"] = "reschedule"
        
        booking = api_get(f"/appointments/{token}")
        doctor_name = booking.get("doctor") # Likely "Dr. Name"
        
        all_doctors = api_get("/doctors")
        
        doctor_id = None
        if doctor_name:
            for d in all_doctors:
                # Robust matching: Strip, Case Ignored.
                if d["name"].lower().strip() == doctor_name.lower().strip():
                    doctor_id = d["id"]
                    break
        
        if doctor_id:
            context.user_data["doctor_id"] = doctor_id
            await show_calendar(query, context)
        else:
            await query.edit_message_text(
                f"⚠️ Cannot reschedule automatically: Doctor '{doctor_name}' not found in current database.\n(Start a new booking instead).",
                reply_markup=InlineKeyboardMarkup([
                    [InlineKeyboardButton("🔙 Back", callback_data="pb_details")]
                ])
            )

async def handle_booking_start(update, context):
    query = update.callback_query
    await query.answer()
    await show_calendar(query, context)

async def show_calendar(query, context, year=None, month=None):
    current_date = datetime.today()
    if year is None: year = current_date.year
    if month is None: month = current_date.month

    # Generate Calendar
    cal = calendar.Calendar(firstweekday=0) # Monday first
    month_days = cal.monthdayscalendar(year, month)
    
    month_name = calendar.month_name[month]
    
    buttons = []
    
    # Month Navigation
    buttons.append([
        InlineKeyboardButton("<<", callback_data=f"cal_prev_{year}_{month}"),
        InlineKeyboardButton(f"{month_name} {year}", callback_data="noop"),
        InlineKeyboardButton(">>", callback_data=f"cal_next_{year}_{month}")
    ])
    
    # Days Grid Header
    buttons.append([InlineKeyboardButton(d, callback_data="noop") for d in ["Mo", "Tu", "We", "Th", "Fr", "Sa", "Su"]])
    
    for week in month_days:
        row = []
        for day in week:
            if day == 0:
                row.append(InlineKeyboardButton(" ", callback_data="noop"))
            else:
                # Disable past dates
                d_obj = datetime(year, month, day)
                if d_obj.date() < current_date.date():
                    row.append(InlineKeyboardButton("❌", callback_data="noop"))
                else:
                    date_str = d_obj.strftime("%Y-%m-%d")
                    row.append(InlineKeyboardButton(str(day), callback_data=f"date_{date_str}"))
        buttons.append(row)

    # Back Button
    doctor_id = context.user_data.get("doctor_id")
    if doctor_id:
        buttons.append([InlineKeyboardButton("🔙 Back to Doctor", callback_data=f"doc_{doctor_id}")])
    else:
        buttons.append([InlineKeyboardButton("🔙 Back to Menu", callback_data="menu_book")])

    await query.edit_message_text(
        "📅 Select a preferred date:",
        reply_markup=InlineKeyboardMarkup(buttons)
    )

async def handle_calendar_nav(update, context):
    query = update.callback_query
    await query.answer()
    
    data = query.data
    _, direction, year, month = data.split("_")
    year, month = int(year), int(month)
    
    if direction == "prev":
        month -= 1
        if month < 1:
            month = 12
            year -= 1
    elif direction == "next":
        month += 1
        if month > 12:
            month = 1
            year += 1
            
    await show_calendar(query, context, year, month)

async def handle_date(update, context):
    query = update.callback_query
    await query.answer()

    date = query.data.replace("date_", "")
    context.user_data["date"] = date

    slots = api_get("/availability", {
        "doctor_id": context.user_data["doctor_id"],
        "date": date
    })

    if not slots:
        await query.edit_message_text(
            f"❌ No slots available on {date}.\nPlease choose another date.",
            reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("🔙 Back to Calendar", callback_data="start_book")]])
        )
        return

    # 3-column grid for slots
    keyboard = []
    row = []
    for s in slots:
        row.append(InlineKeyboardButton(s, callback_data=f"slot_{s}"))
        if len(row) == 3:
            keyboard.append(row)
            row = []
    if row:
        keyboard.append(row)
    
    keyboard.append([InlineKeyboardButton("🔙 Back to Calendar", callback_data="start_book")])

    await query.edit_message_text(
        f"⏰ Select a time slot for {date}:",
        reply_markup=InlineKeyboardMarkup(keyboard)
    )

async def handle_slot(update, context):
    query = update.callback_query
    await query.answer()

    time = query.data.replace("slot_", "")
    payload = {
        "doctor_id": context.user_data["doctor_id"],
        "date": context.user_data["date"],
        "time": time,
        "telegram_id": update.effective_user.id
    }

    booking = api_post("/appointments", payload)
    pdf_url = booking.get("pdf_url", "")

    await query.edit_message_text(
        f"✅ *Appointment Confirmed*\n\n"
        f"📅 {booking['date']} at {booking['time']}\n"
        f"👨‍⚕️ {booking['doctor']}\n\n"
        f"📆 Add to Calendar:\n{booking['calendar_link']}\n"
        f"📥 [Download Receipt]({pdf_url})",
        parse_mode="Markdown"
    )

# ================= POST BOOKING =================

async def handle_post_booking(update, context):
    query = update.callback_query
    await query.answer()
    token = context.user_data["token"]

    if query.data == "pb_details":
        booking = api_get(f"/appointments/{token}")
        pdf_url = booking.get("pdf_url", "")
        
        text = (
            f"📄 *Appointment Details*\n\n"
            f"👨‍⚕️ {booking['doctor']}\n"
            f"📅 {booking['date']} {booking['time']}\n"
            f"📥 [Download Receipt]({pdf_url})"
        )
        await query.edit_message_text(text, parse_mode="Markdown")

    elif query.data == "pb_reschedule":
        context.user_data["mode"] = "reschedule"
        
        booking = api_get(f"/appointments/{token}")
        doctor_name = booking.get("doctor")
        
        all_doctors = api_get("/doctors")
        
        doctor_id = None
        if doctor_name:
            for d in all_doctors:
                if d["name"] == doctor_name:
                    doctor_id = d["id"]
                    break
        
        if doctor_id:
            context.user_data["doctor_id"] = doctor_id
            await show_calendar(query, context)
        else:
            await query.edit_message_text(
                "⚠️ Cannot reschedule: Doctor not found.\nPlease cancel and re-book.",
                reply_markup=InlineKeyboardMarkup([
                    [InlineKeyboardButton("🔙 Back", callback_data="pb_details")]
                ])
            )

    elif query.data == "pb_cancel":
        # Confirmation Dialog
        keyboard = [
            [InlineKeyboardButton("✅ Yes, Cancel", callback_data="confirm_cancel")],
            [InlineKeyboardButton("🚫 No, Keep", callback_data="pb_details")]
        ]
        await query.edit_message_text(
            "⚠️ *Are you sure you want to cancel?*",
            parse_mode="Markdown",
            reply_markup=InlineKeyboardMarkup(keyboard)
        )

async def handle_cancel_confirm(update, context):
    query = update.callback_query
    await query.answer()
    
    token = context.user_data.get("token")
    if token:
        api_delete(f"/appointments/{token}")
        await query.edit_message_text("❌ Appointment cancelled successfully.")
    else:
        await query.edit_message_text("Error: Token lost.")

# ================= MAIN =================

def main():
    if not BOT_TOKEN:
        print("Error: BOT_TOKEN is not set.")
        return

    app = ApplicationBuilder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(handle_menu, pattern="^menu_"))
    
    app.add_handler(CallbackQueryHandler(handle_doctor, pattern="^doc_"))
    app.add_handler(CallbackQueryHandler(handle_booking_start, pattern="^start_book"))
    app.add_handler(CallbackQueryHandler(handle_back_to_doctors, pattern="^back_docs"))
    
    app.add_handler(CallbackQueryHandler(handle_calendar_nav, pattern="^cal_"))
    app.add_handler(CallbackQueryHandler(handle_date, pattern="^date_"))
    app.add_handler(CallbackQueryHandler(handle_slot, pattern="^slot_"))
    
    app.add_handler(CallbackQueryHandler(handle_post_booking, pattern="^pb_"))
    app.add_handler(CallbackQueryHandler(handle_cancel_confirm, pattern="^confirm_cancel"))
    
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_text))

    print("🤖 Bot running...")
    app.run_polling()

if __name__ == "__main__":
    main()
