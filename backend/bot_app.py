import os
import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler, CallbackQueryHandler, MessageHandler, filters
from dotenv import load_dotenv
from bot_client import get_appointment_by_token, cancel_appointment_api, reschedule_appointment
from datetime import datetime
from services.ai_service import extract_specialization
from services.doctor_service import get_doctors_by_specialization

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

BOT_TOKEN = os.getenv("BOT_TOKEN")

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data.clear()
    args = context.args

    # 🔹 CASE 1: User came with token (post-booking)
    if args and args[0].startswith("token_"):
        token = args[0].replace("token_", "")
        appt = get_appointment_by_token(token)

        if not appt:
            await update.message.reply_text("❌ Invalid or expired appointment token.")
            return

        context.user_data["mode"] = "post_booking"
        context.user_data["token"] = token
        
        # Immediately send menu for post-booking
        await send_post_booking_menu(update, appt)
        return

    # 🔹 CASE 2: Normal entry (Contact page / direct open)
    context.user_data["mode"] = "idle"
    keyboard = [
        [InlineKeyboardButton("📅 Book Appointment", callback_data="book")],
        [InlineKeyboardButton("📞 Contact Hospital", callback_data="contact")]
    ]
    
    await update.message.reply_text(
        "👋 Welcome to *ProHealth Hospital Assistant*\n\n"
        "How can I help you today?",
        parse_mode='Markdown',
        reply_markup=InlineKeyboardMarkup(keyboard)
    )

async def send_post_booking_menu(update: Update, appt: dict):
    text = (
        f"✅ *Appointment Found*\n\n"
        f"👤 *Patient:* {appt['patient_name']}\n"
        f"🩺 *Service:* {appt['service']}\n"
        f"👨‍⚕️ *Doctor:* {appt['doctor']}\n"
        f"📅 *Date:* {appt['appointment_datetime']}\n"
        f"🎫 *Token:* `{appt['token']}`\n"
        f"ℹ️ *Status:* {appt['status']}\n\n"
        "What would you like to do?"
    )
    
    keyboard = [
        [InlineKeyboardButton("📄 View Details", callback_data="view")],
        [InlineKeyboardButton("🔁 Reschedule Appointment", callback_data="reschedule")],
        [InlineKeyboardButton("❌ Cancel Appointment", callback_data="cancel")],
        [InlineKeyboardButton("📎 Upload Prescription", callback_data="prescription")]
    ]
    
    # Check if update is from callback or message
    if update.callback_query:
        await update.callback_query.edit_message_text(text, parse_mode='Markdown', reply_markup=InlineKeyboardMarkup(keyboard))
    else:
        await update.message.reply_text(text, parse_mode='Markdown', reply_markup=InlineKeyboardMarkup(keyboard))

async def handle_book(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    context.user_data.clear()
    context.user_data["mode"] = "booking"

    await query.edit_message_text(
        "🩺 Please tell me your health concern or reason for visit.\n"
        "(e.g., 'I have a severe headache' or 'Stomach pain')"
    )

async def handle_contact(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    await query.edit_message_text(
        "📞 *Contact ProHealth Hospital*\n\n"
        "Phone: +91 98765 43210\n"
        "Email: support@prohealth.com\n\n"
        "If our phone line is busy, you can continue using this assistant for instant support.",
        parse_mode="Markdown"
    )

async def handle_post_booking_actions(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    
    token = context.user_data.get("token")
    data = query.data
    
    if data == "view":
        appt = get_appointment_by_token(token)
        if appt:
            await send_post_booking_menu(update, appt)
        else:
            await query.edit_message_text("❌ Error fetching details.")

    elif data == "cancel":
        keyboard = [
            [
                InlineKeyboardButton("✅ Yes, Cancel", callback_data="confirm_cancel"),
                InlineKeyboardButton("❌ No", callback_data="view")
            ]
        ]
        await query.edit_message_text(
            "⚠️ Are you sure you want to cancel this appointment?",
            reply_markup=InlineKeyboardMarkup(keyboard)
        )

    elif data == "confirm_cancel":
        success = cancel_appointment_api(token)
        if success:
            await query.edit_message_text(
                "❌ Appointment cancelled successfully.\n\nIf you need anything else, type /start.",
                parse_mode="Markdown"
            )
        else:
            await query.edit_message_text("⚠️ Unable to cancel appointment.")

    elif data == "reschedule":
        context.user_data["mode"] = "reschedule_input"
        
        await query.edit_message_text(
            "🗓 Please enter the new date and time.\n\n"
            "Format:\n"
            "`YYYY-MM-DD HH:MM`\n\n"
            "Example:\n"
            "`2025-01-12 10:30`",
            parse_mode="Markdown"
        )

async def handle_prescription(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    await query.edit_message_text(
        "📎 Please upload your prescription as an image or PDF.\n(Reminders will be enabled after review.)"
    )

async def handle_text(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text.strip()
    mode = context.user_data.get("mode")

    # 🔹 BOOKING FLOW
    if mode == "booking":
        await handle_booking_with_llm(update, context, text)
        return

    # 🔹 RESCHEDULE INPUT
    if mode == "reschedule_input":
        await handle_reschedule_input(update, context, text)
        return

    # 🔹 FALLBACK
    await update.message.reply_text(
        "Please choose an option from the menu or type *Hi* to start again.",
        parse_mode="Markdown"
    )

async def handle_booking_with_llm(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("🔍 Understanding your concern...")

    # Use AI service
    specialization = extract_specialization(update.message.text)
    context.user_data["specialization"] = specialization

    doctors = get_doctors_by_specialization(specialization)

    if not doctors:
        await update.message.reply_text(
            f"Sorry, no doctors found for *{specialization}*.",
            parse_mode="Markdown"
        )
        return

    # Simply list doctors as an example (since full flow details weren't provided in snippet)
    # Ideally checking doctor details to book
    keyboard = []
    for d in doctors:
        keyboard.append([InlineKeyboardButton(f"{d['name']} ({d['experience']})", callback_data=f"book_doc_{d['id']}")])
    
    await update.message.reply_text(
        f"🩺 Based on your concern, I recommend *{specialization}*.\n"
        "Please choose a specialist:",
        parse_mode="Markdown",
        reply_markup=InlineKeyboardMarkup(keyboard)
    )

async def handle_reschedule_input(update: Update, context: ContextTypes.DEFAULT_TYPE, text_input: str):
    try:
        new_dt = datetime.strptime(text_input, "%Y-%m-%d %H:%M")
    except ValueError:
        await update.message.reply_text(
            "❌ Invalid format.\nPlease use: `YYYY-MM-DD HH:MM`\nExample: `2025-01-12 10:30`",
            parse_mode="Markdown"
        )
        return

    token = context.user_data.get("token")
    if not token:
            await update.message.reply_text("⚠️ Session expired. Please start again from the website link.")
            return

    success = reschedule_appointment(token, new_dt.isoformat())

    if success:
        context.user_data["mode"] = "post_booking"
        await update.message.reply_text(
            f"✅ Appointment rescheduled successfully.\n\n"
            f"📅 New Date & Time:\n{new_dt.strftime('%d %b %Y, %I:%M %p')}"
        )
    else:
        await update.message.reply_text(
            "⚠️ Unable to reschedule. Please try again."
        )

# Placeholder for doctor selection callback if implemented
async def handle_doctor_selection(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    await query.edit_message_text("✅ Doctor selected! (Detailed booking flow placeholder)")

if __name__ == '__main__':
    if not BOT_TOKEN:
        print("Error: BOT_TOKEN is not set in environment variables.")
        exit(1)
        
    application = ApplicationBuilder().token(BOT_TOKEN).build()
    
    application.add_handler(CommandHandler('start', start))
    application.add_handler(CallbackQueryHandler(handle_book, pattern="^book$"))
    application.add_handler(CallbackQueryHandler(handle_contact, pattern="^contact$"))
    
    # Post-booking handlers
    application.add_handler(CallbackQueryHandler(handle_post_booking_actions, pattern="^(view|cancel|confirm_cancel|reschedule)$"))
    application.add_handler(CallbackQueryHandler(handle_prescription, pattern="^prescription$"))
    
    # Booking flow handlers
    application.add_handler(CallbackQueryHandler(handle_doctor_selection, pattern="^book_doc_"))
    
    # Text handler used for both booking concern and reschedule input
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_text))
    
    print("Bot is polling...")
    application.run_polling()
