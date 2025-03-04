from pyrogram import Client, filters
from pyrogram.handlers import MessageHandler, CallbackQueryHandler
from bot.utils.config import API_ID, API_HASH, BOT_TOKEN
from bot.handlers.start import start, newpost, addnew, mychannels, mygroups, delete
from bot.handlers.handler import (select_channel_group, add_channel_group, handle_forwarded_message)
from bot.utils.database import init_db

# ✅ Initialize Database
init_db()

# ✅ Create Bot Client & Add `user_data` Dictionary
app = Client("telegram_bot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)
app.user_data = {}  # ✅ Store user states

# ✅ Register Handlers in Correct Order
app.add_handler(MessageHandler(start, filters.command("start") & filters.private))
app.add_handler(MessageHandler(newpost, filters.command("newpost") & filters.private))
app.add_handler(MessageHandler(addnew, filters.command("addnew") & filters.private))
app.add_handler(MessageHandler(mychannels, filters.command("mychannels") & filters.private))
app.add_handler(MessageHandler(mygroups, filters.command("mygroups") & filters.private))
app.add_handler(MessageHandler(delete, filters.command("delete") & filters.private))


# ✅ "Add Channel" and "Add Group" - Must Be Registered Before Receiving Messages
app.add_handler(CallbackQueryHandler(select_channel_group, filters.regex("^📝 Create Post$")))
app.add_handler(CallbackQueryHandler(add_channel_group, filters.regex("^add_channel_group$")))
app.add_handler(MessageHandler(select_channel_group, filters.private & (filters.text | filters.forwarded)))

app.add_handler(MessageHandler(handle_forwarded_message, filters.private & (filters.text | filters.forwarded)))
# ✅ Start the Bot
if __name__ == "__main__":
    print("✅ Bot started...")
    app.run()

