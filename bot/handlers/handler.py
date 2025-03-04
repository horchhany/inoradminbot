from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery, Message
from bot.utils.database import save_ch_gp, get_channel_group
from validation.validation import Validation
from pyrogram.errors import ChatAdminRequired

# ✅ Store user states
user_data = {}

async def is_admin(client, chat_id, user_id):
    try:
        chat = await client.get_chat(chat_id)  # Get chat details
        
        # ✅ Skip checking admin rights if it's a private chat
        if chat.type == "private":
            return False  # Private chats have no admins
        
        member = await client.get_chat_member(chat_id, user_id)
        return member.status in ["administrator", "creator"]
    
    except ChatAdminRequired:
        return False
    except ValueError as e:
        print(f"⚠️ Error in is_admin(): {e}")
        return False

    
@Client.on_callback_query(filters.regex("^add_channel_group$"))
async def add_channel_group(client, query: CallbackQuery):
    user_id = query.from_user.id

    # ✅ Ensure user_data exists for this user
    if user_id not in user_data:
        user_data[user_id] = {}  

    # ✅ Store the step correctly
    user_data[user_id]["step"] = "waiting_for_channel_or_group"

    await query.message.edit_text(
        "📢 Please forward a message from your **channel/group**, or send its **@username** or **t.me/ link**."
    )

"""@Client.on_callback_query(filters.regex("^📝 Create Post$"))
async def select_channel_group(client, query: CallbackQuery):
    user_id = query.from_user.id
   
    if await is_admin(client, query.message.chat.id, user_id):
        await query.message.edit_text("✅ You are an admin. Proceeding...")
    else:
        await query.message.edit_text("❌ You must be an admin to select a channel/group!")
    # ✅ Get saved channel/group from database
    channel_id, channel_name, group_id, group_name = get_channel_group()

    if channel_id or group_id:
        # ✅ If at least one exists, show selection buttons
        keyboard = []

        if channel_id:
            keyboard.append([InlineKeyboardButton(f"📢 {channel_name}", callback_data=f"post_to:{channel_id}")])
        if group_id:
            keyboard.append([InlineKeyboardButton(f"👥 {group_name}", callback_data=f"post_to:{group_id}")])

        keyboard.append([InlineKeyboardButton("❌ Cancel", callback_data="cancel_post")])

        await query.message.edit_text(
            "📢 **Select where to post:**",
            reply_markup=InlineKeyboardMarkup(keyboard)
        )
    else:
        # ❌ No channel/group exists → Redirect to add one
        await add_channel_group(client, query)"""


@Client.on_message(filters.private & (filters.text | filters.forwarded))
async def select_channel_group(client, message: Message):

    user_id = message.from_user.id
   
    if await is_admin(client, message.chat.id, user_id):
        await message.edit_text("✅ You are an admin. Proceeding...")
    else:
        await message.edit_text("❌ You must be an admin to select a channel/group!")
    # ✅ Get saved channel/group from database
    channel_id, channel_name, group_id, group_name = get_channel_group()

    if channel_id or group_id:
        # ✅ If at least one exists, show selection buttons
        keyboard = []

        if channel_id:
            keyboard.append([InlineKeyboardButton(f"📢 {channel_name}", callback_data=f"post_to:{channel_id}")])
        if group_id:
            keyboard.append([InlineKeyboardButton(f"👥 {group_name}", callback_data=f"post_to:{group_id}")])

        keyboard.append([InlineKeyboardButton("❌ Cancel", callback_data="cancel_post")])

        await message.edit_text(
            "📢 **Select where to post:**",
            reply_markup=InlineKeyboardMarkup(keyboard)
        )
    else:
        # ❌ No channel/group exists → Redirect to add one
        await add_channel_group(client, message)

@Client.on_message(filters.private & (filters.text | filters.forwarded))
async def add_channel_group(client, message: Message):
    
    user_id = message.from_user.id
    keyboard = InlineKeyboardMarkup([
                [InlineKeyboardButton("➕ Add Channel | Group", callback_data="add_channel_group")],
                [InlineKeyboardButton("❌ Cancel", callback_data="cancel_post")]
            ])
    await message.reply_text(
        "📢 You need to add a channel or group first.\n"
        "Forward a message from the channel/group or send its **@username** / ID.",
        reply_markup=keyboard
    )
    

    # ✅ Process based on stored user state
    step = user_data[user_id]["step"]
    print(f"🔍 User Step: {step}")

    if step == "waiting_for_channel_or_group":
        await process_add_channel_group(client, message)
        del user_data[user_id]  # ✅ Remove user from session

async def process_add_channel_group(client, message):
    text = message.text.strip()
    user_id = message.from_user.id
    validator = Validation(client)

    # ✅ Extract username, ID, and link
    chat_id, username, link = None, None, None
    if text.startswith("https://t.me/"):
        username = text.replace("https://t.me/", "").strip("/")
        link = text
    elif text.startswith("@"):
        username = text
    elif text.isdigit() or text.startswith("-100"):
        chat_id = int(text)

    # ✅ Resolve username or ID
    try:
        if username:
            chat = await client.get_chat(username)
            chat_id = chat.id
            username = f"@{chat.username}" if chat.username else None
            link = f"https://t.me/{chat.username}" if chat.username else None
        elif chat_id:
            chat = await client.get_chat(chat_id)
            username = f"@{chat.username}" if chat.username else None
            link = f"https://t.me/{chat.username}" if chat.username else None

        chat_name = chat.title
        chat_type = "channel" if chat.type == "channel" else "group"

        # ✅ 1. Check if the user is an admin
        if not await validator.check_admin_rights(user_id, chat_id):
            await message.reply_text("❌ You must be an **admin** to add this channel/group.")
            return

        # ✅ 2. Check for duplicate entries
        if validator.check_duplicate_entry(chat_id, username, link):
            await message.reply_text("⚠️ This channel/group has already been added.")
            return

        # ✅ 3. Validate if input is correct
        is_valid, error_msg = await validator.validate_channel_or_group(chat_id, username, link)
        if not is_valid:
            await message.reply_text(error_msg)
            return

        # ✅ Save to database
        save_ch_gp(chat_id, chat_name, username, link, chat_type)
        await message.reply_text(f"✅ Successfully added {chat_type.capitalize()}: {chat_name}")

    except Exception as e:
        await message.reply_text(f"⚠️ Error: {e}")



# 🔹 Handle Forwarded Messages (Auto-Detect Channel or Group)
@Client.on_message(filters.forwarded & filters.private)
async def handle_forwarded_message(client, message: Message):
    chat = message.forward_from_chat

    if not chat:
        await message.reply_text("⚠️ Please forward a message from a **channel** or **group**.")
        return

    chat_id = chat.id
    chat_name = chat.title
    username = f"@{chat.username}" if chat.username else None
    link = f"https://t.me/{chat.username}" if chat.username else None

    # ✅ Detect type (channel or group)
    chat_type = "channel" if chat.type == "channel" else "group"

    print(f"📢 Saving: ID={chat_id}, Name={chat_name}, Username={username}, Link={link}, Type={chat_type}")

    # ✅ Save to database
    save_ch_gp(chat_id, chat_name, username, link, chat_type)

    await message.reply_text(f"✅ **{chat_type.capitalize()} Added:**\n**Name:** {chat_name}\n**Username:** {username or 'N/A'}")
