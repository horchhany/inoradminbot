from pyrogram import Client, filters
from pyrogram.handlers import MessageHandler, CallbackQueryHandler
from bot.config import API_ID, API_HASH, BOT_TOKEN
from bot.handlers.start import start, handle_buttons
from bot.handlers.handler import add_channel, add_group, handle_forwarded_message
from bot.utils.database import init_db  # Import database setup

# ✅ Initialize database
init_db()

# ✅ Global dictionary for storing user data
user_data = {}

# ✅ Create bot client
app = Client("telegram_bot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)

# ✅ Register Handlers
app.add_handler(MessageHandler(start, filters.command("start") & filters.private))
app.add_handler(MessageHandler(handle_buttons, filters.text & filters.private))
app.add_handler(CallbackQueryHandler(add_channel, filters.regex("^add_channel$")))
app.add_handler(CallbackQueryHandler(add_group, filters.regex("^add_group$")))
app.add_handler(MessageHandler(handle_forwarded_message, filters.forwarded & filters.private))  # ✅ Fixed filter

# ✅ Run the bot
if __name__ == "__main__":
    print("✅ Bot started...")
    app.run()
