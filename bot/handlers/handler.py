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

    print(f"🔹 Received Message: {message.text or 'Forwarded Message'} from {user_id}")

    if user_id not in client.user_data:
        print("⚠️ User state not found! Maybe user_data is not shared?")
        await message.reply_text("⚠️ Please click 'Add Channel' or 'Add Group' first!")
        return

    step = client.user_data[user_id]["step"]
    print(f"🔍 User Step Detected: {step}")  

    if message.forward_from_chat:
        chat = message.forward_from_chat
        chat_id = chat.id
        chat_name = chat.title
        username = f"@{chat.username}" if chat.username else f"ID: {chat_id}"

        print(f"📢 Detected Forwarded Chat - ID: {chat_id}, Name: {chat_name}, Username: {username}")

        if step == "waiting_for_channel" and chat.type == "channel":
            save_channel(chat_id, chat_name, username)
            await message.reply_text(f"✅ Channel Added: {username}")

        elif step == "waiting_for_group" and chat.type in ["supergroup", "group"]:
            save_group(chat_id, chat_name, username)
            await message.reply_text(f"✅ Group Added: {username}")

        else:
            await message.reply_text("⚠️ Unsupported chat type. Please forward a message from a **channel** or **group**.")

        del client.user_data[user_id]  # ✅ Remove user state after saving
        return

    # If user manually types username or ID
    text = message.text.strip()
    if step == "waiting_for_channel":
        if text.startswith("@"):  # Username
            chat_id = text
            chat_name = "Unknown"
            username = text
        elif text.isdigit():  # Channel ID
            chat_id = int(text)
            chat_name = "Unknown"
            username = f"ID: {chat_id}"
        else:
            print("⚠️ Invalid channel format!")
            await message.reply_text("⚠️ Invalid username or ID. Please send a valid **@username** or numeric **ID**.")
            return

        print(f"📢 Manually Entered Channel - ID: {chat_id}, Username: {username}")
        save_channel(chat_id, chat_name, username)
        await message.reply_text(f"✅ Channel Added: {username}")
        del client.user_data[user_id]

    elif step == "waiting_for_group":
        if text.startswith("@"):  # Username
            chat_id = text
            chat_name = "Unknown"
            username = text
        elif text.isdigit():  # Group ID
            chat_id = int(text)
            chat_name = "Unknown"
            username = f"ID: {chat_id}"
        else:
            print("⚠️ Invalid group format!")
            await message.reply_text("⚠️ Invalid username or ID. Please send a valid **@username** or numeric **ID**.")
            return

        print(f"👥 Manually Entered Group - ID: {chat_id}, Username: {username}")
        save_group(chat_id, chat_name, username)
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
