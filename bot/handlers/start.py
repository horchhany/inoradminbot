from pyrogram import Client, filters
from pyrogram.types import ReplyKeyboardMarkup, ReplyKeyboardRemove
from bot.handlers.post import post  # Import function

@Client.on_message(filters.command("start") & filters.private)
async def start(client, message):
    keyboard = ReplyKeyboardMarkup(
        [["📝 Create Post", "❌ Cancel"]],
        resize_keyboard=True,
        one_time_keyboard=False
    )
    
    await message.reply_text(
        "👋 Hello! I'm your bot.\n\n"
        "Press **'Create Post'** to start creating a post or **'Cancel'** to stop.",
        reply_markup=keyboard
    )

@Client.on_message(filters.text & filters.private)
async def handle_buttons(client, message):
    if message.text == "📝 Create Post":
        await message.reply_text("Please * follow this by", 
             reply_markup=ReplyKeyboardRemove())
        await post(client, message) # ✅ Start post creation without keyboard
    elif message.text == "❌ Cancel":
        await message.reply_text(
            "❌ Post creation canceled.",
            reply_markup=ReplyKeyboardMarkup([["📝 Create Post"]], resize_keyboard=True)
        )

