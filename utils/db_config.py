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


def convert_sets(obj):
    """Recursively convert all sets in an object to lists."""
    if isinstance(obj, set):
        return list(obj)
    elif isinstance(obj, dict):
        return {k: convert_sets(v) for k, v in obj.items()}
    elif isinstance(obj, list):
        return [convert_sets(i) for i in obj]
    else:
        return obj


def set_config_value(key, new_value):
    """Safely store config values, converting sets to lists before saving."""
    conn = get_db_connection()
    cur = conn.cursor()

    safe_value = convert_sets(new_value) 

    cur.execute("""
        INSERT INTO bot_config (key, value)
        VALUES (%s, %s)
        ON CONFLICT (key) DO UPDATE
        SET value = EXCLUDED.value;
    """, (key, json.dumps(safe_value)))

    conn.commit()
    conn.close()
