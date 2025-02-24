from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery
from bot.utils.database import get_channel_group


# Store user post data
user_posts = {}
 
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

async def select_destination(client, query: CallbackQuery):
    user_id = query.from_user.id
    destination = "channel" if "channel" in query.data else "group"
    
    # Ensure user_posts has a valid structure
    if user_id not in user_posts:
        user_posts[user_id] = {"messages": []}

    user_posts[user_id]["destination"] = destination  # Store choice


@Client.on_message(filters.private & (filters.text | filters.photo | filters.video | filters.sticker))
async def collect_post_content(client, message):
    user_id = message.from_user.id
    
    if user_id in user_posts and "destination" in user_posts[user_id]:
        user_posts[user_id]["messages"].append(message)

        keyboard = InlineKeyboardMarkup([
            [InlineKeyboardButton("✅ Send Now", callback_data="send_post")],
            [InlineKeyboardButton("🗑 Remove Last", callback_data="remove_last_message")],
            [InlineKeyboardButton("❌ Cancel", callback_data="cancel_post")]
        ])

        await message.reply_text("✅ Added! Send more or click 'Send Now'.", reply_markup=keyboard)

@Client.on_callback_query(filters.regex("remove_last_message"))
async def remove_last_message(client, query: CallbackQuery):
    """Removes the last added message before posting."""
    user_id = query.from_user.id

    if user_id in user_posts and user_posts[user_id]["messages"]:
        user_posts[user_id]["messages"].pop()  # Remove last message
        await query.answer("🗑 Removed the last message!", show_alert=True)
    else:
        await query.answer("⚠️ No messages to remove!", show_alert=True)

async def send_post(client, query: CallbackQuery):
    user_id = query.from_user.id

    if user_id not in user_posts or not user_posts[user_id]["messages"]:
        await query.answer("⚠️ No messages to send!", show_alert=True)
        return

    # Fetch the correct destination from the database
    channel_id, _, group_id, _ = get_channel_group()
    destination_id = channel_id if user_posts[user_id]["destination"] == "channel" else group_id

    if not destination_id:
        await query.answer("⚠️ No valid destination found!", show_alert=True)
        return

    # Send all collected messages
    for msg in user_posts[user_id]["messages"]:
        if msg.text:
            await client.send_message(destination_id, msg.text)
        elif msg.photo:
            await client.send_photo(destination_id, msg.photo.file_id, caption=msg.caption or "")
        elif msg.video:
            await client.send_video(destination_id, msg.video.file_id, caption=msg.caption or "")
        elif msg.sticker:
            await client.send_sticker(destination_id, msg.sticker.file_id)

    await query.message.edit_text("✅ Post sent successfully!")
    del user_posts[user_id]  # Clear data after sending


@Client.on_callback_query(filters.regex("cancel_post"))
async def cancel_post(client, query: CallbackQuery):
    """Cancels post creation."""
    user_id = query.from_user.id
    user_posts.pop(user_id, None)
    await query.message.edit_text("❌ Post creation canceled.")
