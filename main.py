import os
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler, ContextTypes
from modules import pnr, route, entertainment, meditation, season_ticket, food_order, vehicle_booking, complaint

TOKEN = os.getenv("BOT_TOKEN")

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [InlineKeyboardButton("🎫 PNR Tracker", callback_data="pnr")],
        [InlineKeyboardButton("🗺️ Route Info", callback_data="route")],
        [InlineKeyboardButton("🎧 Entertainment", callback_data="entertainment")],
        [InlineKeyboardButton("🧘 Meditation & Music", callback_data="meditation")],
        [InlineKeyboardButton("🎟️ Season/Platform Ticket", callback_data="season")],
        [InlineKeyboardButton("🍽️ Food Order", callback_data="food")],
        [InlineKeyboardButton("🚕 Vehicle Booking", callback_data="vehicle")],
        [InlineKeyboardButton("😡 Complaint / Feedback", callback_data="complaint")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text("👋 Welcome to RailSaathi Pro! Choose a service:", reply_markup=reply_markup)

async def handle_click(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    feature_map = {
        "pnr": pnr.respond,
        "route": route.respond,
        "entertainment": entertainment.respond,
        "meditation": meditation.respond,
        "season": season_ticket.respond,
        "food": food_order.respond,
        "vehicle": vehicle_booking.respond,
        "complaint": complaint.respond
    }
    if query.data in feature_map:
        await feature_map[query.data](query)

if __name__ == "__main__":
    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(handle_click))
    print("🚆 RailSaathi Pro is running...")
    app.run_polling()