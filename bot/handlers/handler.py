from pyrogram import Client, filters
from pyrogram.types import CallbackQuery, Message
from bot.utils.database import save_channel, save_group  # Import database functions

# ✅ Store user states
user_data = {}

# ✅ Handle "Add Channel" Button Click
@Client.on_callback_query(filters.regex("^add_channel$"))
async def add_channel(client, query: CallbackQuery):
    user_id = query.from_user.id
    client.user_data[user_id] = {"step": "waiting_for_channel"}  # ✅ Store in `client.user_data`
    print(f"✅ User {user_id} is now in 'waiting_for_channel' state.")  
    await query.message.edit_text("📢 Forward any message from your **channel** to add it, or send its **@username** or ID.")

# ✅ Handle "Add Group" Button Click
@Client.on_callback_query(filters.regex("^add_group$"))
async def add_group(client, query: CallbackQuery):
    user_id = query.from_user.id
    client.user_data[user_id] = {"step": "waiting_for_group"}  # ✅ Store in `client.user_data`
    print(f"✅ User {user_id} is now in 'waiting_for_group' state.")  
    await query.message.edit_text("👥 Forward any message from your **group** to add it, or send its **@username** or ID.")

# ✅ Handle Forwarded or Sent Channel/Group Username or ID
@Client.on_message(filters.private & (filters.text | filters.forwarded))
async def receive_channel_or_group(client, message: Message):
 
    user_id = message.from_user.id
    text = message.text.strip() if message.text else None

    print(f"🟢 Debug: Message received from {user_id}: {text or 'Forwarded Message'}")

    # ✅ Ensure user_data exists
    if not hasattr(client, "user_data"):
        client.user_data = {}

    if user_id not in client.user_data:
        print("⚠️ User state not found!")
        await message.reply_text("⚠️ Please click 'Add Channel' or 'Add Group' first!")
        return

    step = client.user_data[user_id]["step"]
    print(f"🔍 User Step Detected: {step}")  

    if step == "waiting_for_channel":
        print("📢 Processing as Channel...")
        if message.forward_from_chat:  # ✅ Forwarded from a channel
            channel_id = message.forward_from_chat.id
            channel_name = message.forward_from_chat.title
            username = f"@{message.forward_from_chat.username}" if message.forward_from_chat.username else f"ID: {channel_id}"
        else:  # ✅ Manually entered username or ID
            if text.startswith("@"):  # Username
                channel_id = text
                channel_name = "Unknown"
                username = text
            elif text.isdigit():  # Channel ID
                channel_id = int(text)
                channel_name = "Unknown"
                username = f"ID: {channel_id}"
            else:
                print("❌ Invalid username or ID!")
                await message.reply_text("⚠️ Invalid username or ID. Please send a valid **@username** or numeric **ID**.")
                return

        print(f"📢 Saving Channel: {channel_id}, {channel_name}, {username}")
        save_channel(channel_id, channel_name, username)
        await message.reply_text(f"✅ Channel Added: {username}")
        del client.user_data[user_id]  

    elif step == "waiting_for_group":
        print("👥 Processing as Group...")
        if message.forward_from_chat:  # ✅ Forwarded from a group
            group_id = message.forward_from_chat.id
            group_name = message.forward_from_chat.title
            username = f"@{message.forward_from_chat.username}" if message.forward_from_chat.username else f"ID: {group_id}"
        else:  # ✅ Manually entered username or ID
            if text.startswith("@"):  # Username
                group_id = text
                group_name = "Unknown"
                username = text
            elif text.isdigit():  # Group ID
                group_id = int(text)
                group_name = "Unknown"
                username = f"ID: {group_id}"
            else:
                print("❌ Invalid username or ID!")
                await message.reply_text("⚠️ Invalid username or ID. Please send a valid **@username** or numeric **ID**.")
                return

        print(f"👥 Saving Group: {group_id}, {group_name}, {username}")
        save_group(group_id, group_name, username)
        await message.reply_text(f"✅ Group Added: {username}")
        del client.user_data[user_id]

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
