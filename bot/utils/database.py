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
    
    # ✅ Create Tables with Auto-Increment ID
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS ch_gp_name (
            id BIGSERIAL PRIMARY KEY,  
            ch_gp_ID BIGINT UNIQUE,    
            name TEXT,
            username TEXT,
            link TEXT,
            type TEXT   
        )                
    """)
    
    conn.commit()
    cursor.close()
    conn.close()



def save_ch_gp(chat_id, name, username, link, chat_type):
    conn = psycopg2.connect(**DB_CONFIG)
    cursor = conn.cursor()
    
    query = """
        INSERT INTO ch_gp_name (ch_gp_ID, name, username, link, type) 
        VALUES (%s, %s, %s, %s, %s)
    """
    values = (chat_id, name, username, link, chat_type)

    try:
        cursor.execute(query, values)
        conn.commit()
        print(f"✅ Saved to database: {values}")
    except Exception as e:
        print(f"❌ Database error: {e}")
    finally:
        cursor.close()
        conn.close()


def get_channel_group():
    conn = psycopg2.connect(**DB_CONFIG)
    cursor = conn.cursor()

    # ✅ Get Latest Channel
    cursor.execute("SELECT ch_gp_ID, name, username, link FROM ch_gp_name WHERE type = 'channel' ORDER BY id DESC LIMIT 1")
    channel = cursor.fetchone()
    channel_id, channel_name, channel_username, channel_link = channel if channel else (None, None, None, None)

    # ✅ Get Latest Group
    cursor.execute("SELECT ch_gp_ID, name, username, link FROM ch_gp_name WHERE type = 'group' ORDER BY id DESC LIMIT 1")
    group = cursor.fetchone()
    group_id, group_name, group_username, group_link = group if group else (None, None, None, None)

    cursor.close()
    conn.close()

    return channel_id, channel_name, channel_username, channel_link, group_id, group_name, group_username, group_link


def get_channel_group_by_id(chat_id):
    conn = psycopg2.connect(**DB_CONFIG)
    cursor = conn.cursor()
    cursor.execute("SELECT ch_gp_ID FROM ch_gp_name WHERE ch_gp_ID = %s", (chat_id,))
    result = cursor.fetchone()
    cursor.close()
    conn.close()
    return result

def get_channel_group_by_username(username):
    conn = psycopg2.connect(**DB_CONFIG)
    cursor = conn.cursor()
    cursor.execute("SELECT username FROM ch_gp_name WHERE username = %s", (username,))
    result = cursor.fetchone()
    cursor.close()
    conn.close()
    return result

def get_channel_group_by_link(link):
    conn = psycopg2.connect(**DB_CONFIG)
    cursor = conn.cursor()
    cursor.execute("SELECT link FROM ch_gp_name WHERE link = %s", (link,))
    result = cursor.fetchone()
    cursor.close()
    conn.close()
    return result
