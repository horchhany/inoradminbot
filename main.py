import asyncio
from pyrogram import Client, filters
from pyrogram.handlers import MessageHandler, CallbackQueryHandler
from bot.config import API_ID, API_HASH, BOT_TOKEN
from bot.handlers.start import start, handle_buttons
from bot.handlers.handler import add_channel, add_group, receive_channel_or_group, handle_forwarded_message
from bot.utils.database import init_db

# ✅ Initialize Database
init_db()

# ✅ Create Bot Client & Add `user_data` Dictionary
app = Client("telegram_bot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)
app.user_data = {}  # ✅ Add this line to store user steps

# ✅ Register Handlers
app.add_handler(MessageHandler(start, filters.command("start") & filters.private))
app.add_handler(MessageHandler(handle_buttons, filters.text & filters.private))
app.add_handler(CallbackQueryHandler(add_channel, filters.regex("^add_channel$")))
app.add_handler(CallbackQueryHandler(add_group, filters.regex("^add_group$")))
app.add_handler(MessageHandler(receive_channel_or_group, filters.text & filters.private))
app.add_handler(MessageHandler(handle_forwarded_message, filters.forwarded & filters.private))

async def main():
    print("✅ Bot started...")
    await app.start()
    await asyncio.Event().wait()

if __name__ == "__main__":
    app.run(main())
