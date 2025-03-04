from pyrogram import Client
from pyrogram.errors import UsernameNotOccupied, PeerIdInvalid, ChatAdminRequired
from bot.utils.database import get_channel_group_by_id, get_channel_group_by_username, get_channel_group_by_link

class Validation:
    def __init__(self, client: Client):
        self.client = client

    async def check_admin_rights(self, user_id: int, chat_id: int) -> bool:
        """✅ Check if the user is an administrator in the channel or group."""
        try:
            chat_member = await self.client.get_chat_member(chat_id, user_id)
            return chat_member.status in ["creator", "administrator"]
        except ChatAdminRequired:
            return False  # Bot is not an admin
        except Exception as e:
            print(f"⚠️ Admin check error: {e}")
            return False

    def check_duplicate_entry(self, chat_id: int, username: str, link: str) -> bool:
        """✅ Check if the channel/group already exists in the database."""
        if get_channel_group_by_id(chat_id):
            return True
        if username and get_channel_group_by_username(username):
            return True
        if link and get_channel_group_by_link(link):
            return True
        return False

    async def validate_channel_or_group(self, chat_id: int, username: str, link: str):
        """✅ Validate if the channel/group exists and check mismatched input."""
        try:
            chat = await self.client.get_chat(chat_id)

            # ✅ Ensure input values match the actual chat details
            if username and username != f"@{chat.username}":
                return False, "⚠️ The provided username does not match the actual channel/group."
            if link and link != f"https://t.me/{chat.username}":
                return False, "⚠️ The provided link does not match the actual channel/group."

            return True, None

        except (UsernameNotOccupied, PeerIdInvalid):
            return False, "❌ Invalid channel or group. Please check the username, ID, or link."
        except Exception as e:
            return False, f"⚠️ Unexpected error: {e}"
