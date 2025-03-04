from pyrogram import Client, filters
from pyrogram.types import  ReplyKeyboardMarkup, InlineKeyboardMarkup, InlineKeyboardButton


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

@Client.on_message(filters.command("newpost") & filters.private)
async def newpost(client, message):
    keyboard = ReplyKeyboardMarkup(
        [["📝 New Post", "❌ Cancel"]],
        resize_keyboard=True,
        one_time_keyboard=False
    )
    
    await message.reply_text(
        "👋 Hello! I'm your bot.\n\n"
        "Press **'Create Post'** to start creating a post or **'Cancel'** to stop.",
        reply_markup=keyboard
    )
@Client.on_message(filters.command("addnew") & filters.private)
async def addnew(client, message):
    keyboard = ReplyKeyboardMarkup(
        [["➕ Add Channel | Group", "❌ Cancel", ]],
        resize_keyboard=True,
        one_time_keyboard=False,
        
    )
    
    await message.reply_text(
        "Adding a channel\n\n"
        "To add a channel you should follow these two steps:\n\n"

        "1. Add @inoradmin_bot to admins of your channel | group."
        "2. Then forward to me any message from your channel (you can also send me its username or ID)..",
        reply_markup=keyboard
    )

@Client.on_message(filters.command("mychannels") & filters.private)
async def mychannels(client, message):
    keyboard = InlineKeyboardMarkup([
                [InlineKeyboardButton("My Add Channel", callback_data="mychannels")],
               
            ])
    await message.reply_text(
        "📢 Your Channel.",
        reply_markup=keyboard
    )

@Client.on_message(filters.command("groups") & filters.private)
async def mygroups(client, message):
    keyboard = InlineKeyboardMarkup([
                [InlineKeyboardButton("My Add groups", callback_data="groups")],
               
            ])
    await message.reply_text(
        "📢 Your groups.",
        reply_markup=keyboard
    )

@Client.on_message(filters.command("groups") & filters.private)
async def delete(client, message):
    keyboard = InlineKeyboardMarkup([
                [InlineKeyboardButton("My Add delete", callback_data="delete")],
               
            ])
    await message.reply_text(
        "📢 Your delete.",
        reply_markup=keyboard
    )