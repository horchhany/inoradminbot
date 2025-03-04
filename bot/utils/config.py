
import os
from dotenv import load_dotenv

load_dotenv()  # ✅ Load .env file

API_ID = int(os.getenv("API_ID"))
API_HASH = os.getenv("API_HASH")
BOT_TOKEN = os.getenv("BOT_TOKEN")
DATABASE_FILE = os.getenv("DATABASE_FILE", "data/bot.db")  # ✅ Default value
