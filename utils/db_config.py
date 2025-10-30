import os
import psycopg2
import json

def get_db_connection():
    return psycopg2.connect(os.getenv("DATABASE_URL"), sslmode="require")

def get_config_value(key):
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("SELECT value FROM bot_config WHERE key = %s;", (key,))
    result = cur.fetchone()
    conn.close()

    if not result:
        return None

    value = result[0]

    if isinstance(value, dict):
        return value
    if isinstance(value, str):
        try:
            return json.loads(value)
        except json.JSONDecodeError:
            return value
    return value

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