import psycopg2


#postgresql://postgres:FUnjglOteksbADGGXYnLEYfIxdkShJVM@tramway.proxy.rlwy.net:37457/railway
# ✅ Database Configuration
DB_CONFIG = {
    "dbname": "railway",
    "user": "postgres",
    "password": "FUnjglOteksbADGGXYnLEYfIxdkShJVM",
    "host": "tramway.proxy.rlwy.net",  # e.g., "localhost" or server IP
    "port": "37457"     # Default PostgreSQL port is 5432
}

# ✅ Initialize Database

def init_db():
    conn = psycopg2.connect(**DB_CONFIG)
    cursor = conn.cursor()
    
    # ✅ Create Tables
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS channels (
            id BIGINT PRIMARY KEY,
            name TEXT,
            username TEXT
        )
    """)
    
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS groups (
            id BIGINT PRIMARY KEY,
            name TEXT,
            username TEXT
        )
    """)
    
    conn.commit()
    cursor.close()
    conn.close()

# ✅ Save Channel
def save_channel(channel_id, name, username):
    print(f"📢 Saving Channel in Database: ID={channel_id}, Name={name}, Username={username}")
    conn = psycopg2.connect(**DB_CONFIG)
    cursor = conn.cursor()
    
    try:
        cursor.execute(
            "INSERT INTO channels (id, name, username) VALUES (%s, %s, %s) ON CONFLICT (id) DO UPDATE SET name = EXCLUDED.name, username = EXCLUDED.username",
            (channel_id, name, username)
        )
        conn.commit()
        print(f"✅ Channel saved: {name} (@{username})")  # Debugging Log
        return f"✅ Channel **{name}** (@{username}) has been added successfully!"
    except Exception as e:
        print(f"❌ Error saving channel: {e}")  # Debugging Log
        return "❌ Failed to add the channel. Please try again."
    finally:
        cursor.close()
        conn.close()

# ✅ Save Group
def save_group(group_id, name, username):
    print(f"👥 Saving Group in Database: ID={group_id}, Name={name}, Username={username}")
    conn = psycopg2.connect(**DB_CONFIG)
    cursor = conn.cursor()
    
    try:
        cursor.execute(
            "INSERT INTO groups (id, name, username) VALUES (%s, %s, %s) ON CONFLICT (id) DO UPDATE SET name = EXCLUDED.name, username = EXCLUDED.username",
            (group_id, name, username)
        )
        conn.commit()
        print(f"✅ Group saved: {name} (@{username})")  # Debugging Log
        return f"✅ Group **{name}** (@{username}) has been added successfully!"
    except Exception as e:
        print(f"❌ Error saving group: {e}")  # Debugging Log
        return "❌ Failed to add the group. Please try again."
    finally:
        cursor.close()
        conn.close()

# ✅ Get Last Added Channel & Group
def get_channel_group():
    conn = psycopg2.connect(**DB_CONFIG)
    cursor = conn.cursor()

    # Get Latest Channel
    cursor.execute("SELECT id, name FROM channels ORDER BY id DESC LIMIT 1")
    channel = cursor.fetchone()
    channel_id, channel_name = channel if channel else (None, None)

    # Get Latest Group
    cursor.execute("SELECT id, name FROM groups ORDER BY id DESC LIMIT 1")
    group = cursor.fetchone()
    group_id, group_name = group if group else (None, None)

    cursor.close()
    conn.close()
    return channel_id, channel_name, group_id, group_name  # ✅ Returns (channel_id, channel_name, group_id, group_name)
