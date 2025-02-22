from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery
from bot.config import CHANNEL_ID, GROUP_ID


# Store user post data
user_posts = {}
 
@Client.on_callback_query(filters.regex("select_(channel|group)"))
async def select_destination(client, query: CallbackQuery):
    """User selects Channel or Group for posting."""
    user_id = query.from_user.id
    destination = "channel" if "channel" in query.data else "group"
    
    user_posts[user_id] = {
        "destination": destination,
        "messages": []  # Store multiple messages
    }

    await query.message.edit_text(
        "📩 Send me one or multiple messages you want to include in the post.\n"
        "It can be anything — text, photo, video, even a sticker.\n\n"
        "When you're done, click '✅ Send Now'.",
        reply_markup=InlineKeyboardMarkup([
            [InlineKeyboardButton("✅ Send Now", callback_data="send_post")],
            [InlineKeyboardButton("❌ Cancel", callback_data="cancel_post")]
        ])
    )

@Client.on_message(filters.private & (filters.text | filters.photo | filters.video | filters.sticker))
async def collect_post_content(client, message):
    """Collects multiple messages (text, photo, video, stickers)."""
    user_id = message.from_user.id
    
    if user_id in user_posts and "destination" in user_posts[user_id]:
        user_posts[user_id]["messages"].append(message)

        await message.reply_text("✅ Added! Send more or click 'Send Now'.")

@Client.on_callback_query(filters.regex("send_post"))
async def send_post(client, query: CallbackQuery):
    """Sends the collected post to the selected destination (Channel or Group)."""
    user_id = query.from_user.id

    if user_id not in user_posts or not user_posts[user_id]["messages"]:
        await query.answer("⚠️ No messages to send!", show_alert=True)
        return

    destination_id = CHANNEL_ID if user_posts[user_id]["destination"] == "channel" else GROUP_ID

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
