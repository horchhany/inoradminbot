from pyrogram import Client, filters
from pyrogram.handlers import MessageHandler, CallbackQueryHandler
from bot.config import API_ID, API_HASH, BOT_TOKEN
from bot.handlers.start import start, handle_buttons
from bot.handlers.handler import (
    add_channel, add_group, receive_channel_or_group, handle_forwarded_message
)
from bot.utils.database import init_db
# ✅ Initialize Database
init_db()

# ✅ Create Bot Client & Add `user_data` Dictionary
app = Client("telegram_bot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)
app.user_data = {}  # ✅ Store user states

# ✅ Register Handlers in Correct Order
app.add_handler(MessageHandler(start, filters.command("start") & filters.private))
app.add_handler(MessageHandler(handle_buttons, filters.text & filters.private))

# ✅ "Add Channel" and "Add Group" - Must Be Registered Before Receiving Messages
app.add_handler(CallbackQueryHandler(add_channel, filters.regex("^add_channel$")))
app.add_handler(CallbackQueryHandler(add_group, filters.regex("^add_group$")))

# ✅ Receiving Username/ID or Forwarded Messages
app.add_handler(MessageHandler(receive_channel_or_group, filters.private & (filters.text | filters.forwarded)))
app.add_handler(MessageHandler(handle_forwarded_message, filters.forwarded & filters.private))

# ✅ Start the Bot
if __name__ == "__main__":
    print("✅ Bot started...")
    app.run()
