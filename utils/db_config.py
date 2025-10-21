import os
import psycopg2
import json

def get_db_connection():
    return psycopg2.connect(os.getenv("DATABASE_URL"))

def get_config_value(key):
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("SELECT value FROM bot_config WHERE key = %s;", (key,))
    result = cur.fetchone()
    conn.close()
    if result:
        return result[0]
    return None

def set_config_value(key, new_value):
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("""
        INSERT INTO bot_config (key, value)
        VALUES (%s, %s)
        ON CONFLICT (key) DO UPDATE
        SET value = EXCLUDED.value;
    """, (key, json.dumps(new_value)))
    conn.commit()
    conn.close()
