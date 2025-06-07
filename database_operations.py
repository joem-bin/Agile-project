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

def get_user(username, password):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT user_id, role FROM users WHERE username = ? AND password = ?", (username, password))
    user = cursor.fetchone()
    conn.close()
    return user

def get_tickets_for_user(user_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(
        "SELECT * FROM tickets WHERE user_id = ? AND status != 'closed'",
        (user_id,)
    )
    tickets = cursor.fetchall()
    conn.close()
    return tickets


def get_all_tickets():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM tickets")
    tickets = cursor.fetchall()
    conn.close()
    return tickets

def get_ticket(ticket_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM tickets WHERE ticket_id = ?", (ticket_id,))
    ticket = cursor.fetchone()
    conn.close()
    return ticket

def get_comments(ticket_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM comments WHERE ticket_id = ?", (ticket_id,))
    comments = cursor.fetchall()
    conn.close()
    return comments

def get_categories():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT category_id, category_name FROM categories")
    categories = cursor.fetchall()
    conn.close()
    return categories

def close_ticket(ticket_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("UPDATE tickets SET status = 'closed' WHERE ticket_id = ?", (ticket_id,))
    conn.commit()
    conn.close()

def insert_comment(ticket_id, user_id, message):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO comments (ticket_id, user_id, message) VALUES (?, ?, ?)",
        (ticket_id, user_id, message)
    )
    conn.commit()
    conn.close()


