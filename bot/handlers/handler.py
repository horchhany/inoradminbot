from pyrogram import Client, filters
from pyrogram.types import CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton, Message
from bot.utils.database import save_channel, save_group, get_channel_group  # Import database functions

# ✅ Store user states
user_data = {}

async def post(client, message):
    # 🔹 Fetch stored channels and groups
    channel_id, channel_name, group_id, group_name = get_channel_group()

    if channel_id and group_id:
        keyboard = InlineKeyboardMarkup([
            [InlineKeyboardButton(f"📢 {channel_name}", callback_data=f"select_channel:{channel_id}"),
             InlineKeyboardButton(f"👥 {group_name}", callback_data=f"select_group:{group_id}")],
            [InlineKeyboardButton("❌ Cancel", callback_data="cancel_post")]
        ])
        await message.reply_text("📢 Select where to post:", reply_markup=keyboard)
    else:
        keyboard = InlineKeyboardMarkup([
            [InlineKeyboardButton("➕ Add Channel", callback_data="add_channel"),
             InlineKeyboardButton("➕ Add Group", callback_data="add_group")],
            [InlineKeyboardButton("❌ Cancel", callback_data="cancel_post")]
        ])
        await message.reply_text(
            "Adding Channel | Group\n\n"
            "To add, follow these steps:\n"
            "1. Add **'BOT'** as an admin in your channel/group.\n"
            "2. Forward a message from the channel/group, or send its username/ID.",
            reply_markup=keyboard
        )

# 🔹 Handle "Add Channel" Button Click
@Client.on_callback_query(filters.regex("^add_channel$"))
async def add_channel(client, query: CallbackQuery):
    user_id = query.from_user.id
    user_data[user_id] = {"step": "waiting_for_channel"}  # ✅ Store user state
    await query.message.edit_text("📢 Forward any message from your **channel** to add it, or send its **@username** or ID.")

# 🔹 Handle "Add Group" Button Click
@Client.on_callback_query(filters.regex("^add_group$"))
async def add_group(client, query: CallbackQuery):
    user_id = query.from_user.id
    user_data[user_id] = {"step": "waiting_for_group"}  # ✅ Store user state
    await query.message.edit_text("👥 Forward any message from your **group** to add it, or send its **@username** or ID.")

# 🔹 Handle Forwarded Messages (Auto-Detect Channel or Group)
@Client.on_message(filters.forwarded & filters.private)
async def handle_forwarded_message(client, message: Message):
    chat = message.forward_from_chat

    if not chat:
        await message.reply_text("⚠️ Please forward a message from a **channel** or **group**.")
        return

    if chat.type == "channel":
        save_channel(chat.id, chat.title, chat.username)
        await message.reply_text(f"✅ **Channel Added:**\n**Name:** {chat.title}\n**Username:** @{chat.username if chat.username else 'N/A'}")
    
    elif chat.type in ["supergroup", "group"]:
        save_group(chat.id, chat.title, chat.username)
        await message.reply_text(f"✅ **Group Added:**\n**Name:** {chat.title}\n**Username:** @{chat.username if chat.username else 'N/A'}")
    
    else:
        await message.reply_text("⚠️ Unsupported chat type.")

# 🔹 Handle Manual Channel/Group ID Submission
@Client.on_message(filters.text & filters.private)
async def receive_channel_or_group(client, message):
    user_id = message.from_user.id

    if user_id in user_data:
        step = user_data[user_id]["step"]

        if step == "waiting_for_channel":
            # ✅ Save to database
            save_channel(message.text, "Unknown", message.text)
            await message.reply_text(f"✅ **Channel Added:**\n**ID/Username:** `{message.text}`")
            del user_data[user_id]  # Remove user state

        elif step == "waiting_for_group":
            # ✅ Save to database
            save_group(message.text, "Unknown", message.text)
            await message.reply_text(f"✅ **Group Added:**\n**ID/Username:** `{message.text}`")
            del user_data[user_id]  # Remove user state
