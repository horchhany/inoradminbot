import sqlite3
import os

DB_FILE = "data/bot.db"

# ✅ Ensure Database Directory Exists
os.makedirs("data", exist_ok=True)

# ✅ Initialize Database
def init_db():
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    
    # ✅ Create Tables
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS channels (
            id INTEGER PRIMARY KEY,
            name TEXT,
            username TEXT
        )
    """)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS groups (
            id INTEGER PRIMARY KEY,
            name TEXT,
            username TEXT
        )
    """)
    
    conn.commit()
    conn.close()

# ✅ Save Channel
def save_channel(channel_id, name, username, channel_name):
    print(f"📢 Saving Channel in Database: ID={channel_id}, Name={channel_name}, Username={username}")
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    
    try:
        cursor.execute("INSERT OR REPLACE INTO channels (id, name, username) VALUES (?, ?, ?)",
                       (channel_id, name, username))
        conn.commit()
        print(f"✅ Channel saved: {name} ({username})")  # Debugging Log
        return f"✅ Channel **{name}** (@{username}) has been added successfully!"
    except Exception as e:
        print(f"❌ Error saving channel: {e}")  # Debugging Log
        return "❌ Failed to add the channel. Please try again."
    finally:
        conn.close()


# ✅ Save Group
def save_group(group_id, name, username, group_name):
    print(f"👥 Saving Group in Database: ID={group_id}, Name={group_name}, Username={username}")
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    
    try:
        cursor.execute("INSERT OR REPLACE INTO groups (id, name, username) VALUES (?, ?, ?)",
                       (group_id, name, username))
        conn.commit()
        print(f"✅ Group saved: {name} ({username})")  # Debugging Log
        return f"✅ Group **{name}** (@{username}) has been added successfully!"
    except Exception as e:
        print(f"❌ Error saving group: {e}")  # Debugging Log
        return "❌ Failed to add the group. Please try again."
    finally:
        conn.close()


# ✅ Get Last Added Channel & Group
def get_channel_group():
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()

    # Get Latest Channel
    cursor.execute("SELECT id, name FROM channels ORDER BY id DESC LIMIT 1")
    channel = cursor.fetchone()  
    channel_id, channel_name = channel if channel else (None, None)

    # Get Latest Group
    cursor.execute("SELECT id, name FROM groups ORDER BY id DESC LIMIT 1")
    group = cursor.fetchone()  
    group_id, group_name = group if group else (None, None)

    conn.close()
    return channel_id, channel_name, group_id, group_name  # ✅ Returns (channel_id, channel_name, group_id, group_name)
