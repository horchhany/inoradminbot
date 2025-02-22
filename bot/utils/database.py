import sqlite3

def init_db():
    conn = sqlite3.connect("bot_data.db")
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS channels (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            channel_id TEXT UNIQUE,
            name TEXT,
            username TEXT
        )
    """)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS groups (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            group_id TEXT UNIQUE,
            name TEXT,
            username TEXT
        )
    """)
    conn.commit()
    conn.close()

def save_channel(channel_id, name, username):
    conn = sqlite3.connect("bot_data.db")
    cursor = conn.cursor()
    cursor.execute("INSERT OR REPLACE INTO channels (channel_id, name, username) VALUES (?, ?, ?)", (channel_id, name, username))
    conn.commit()
    conn.close()
    return f"✅ Channel **{name}** (@{username}) has been added successfully!"

def save_group(group_id, name, username):
    conn = sqlite3.connect("bot_data.db")
    cursor = conn.cursor()
    cursor.execute("INSERT OR REPLACE INTO groups (group_id, name, username) VALUES (?, ?, ?)", (group_id, name, username))
    conn.commit()
    conn.close()
    return f"✅ Group **{name}** (@{username}) has been added successfully!"

def get_channel_group():
    conn = sqlite3.connect("bot_data.db")
    cursor = conn.cursor()
    
    cursor.execute("SELECT channel_id, name FROM channels ORDER BY id DESC LIMIT 1")
    channel = cursor.fetchone()
    channel_id, channel_name = channel if channel else (None, None)
    
    cursor.execute("SELECT group_id, name FROM groups ORDER BY id DESC LIMIT 1")
    group = cursor.fetchone()
    group_id, group_name = group if group else (None, None)

    conn.close()
    return channel_id, channel_name, group_id, group_name
