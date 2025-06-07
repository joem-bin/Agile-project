import sqlite3
from datetime import datetime

DB_NAME = "test.db"

def get_db_connection():
    return sqlite3.connect(DB_NAME)

def insert_ticket(user_id, category_id, title, description, status='open'):
    created_at = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO tickets (user_id, category_id, title, description, status, created_at)
        VALUES (?, ?, ?, ?, ?, ?)
    """, (user_id, category_id, title, description, status, created_at))

    conn.commit()
    conn.close()

    print(f"Inserted ticket for user_id {user_id} with status '{status}'.")
