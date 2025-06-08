import sqlite3
from datetime import datetime
import bcrypt




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



def insert_user(username, email, password, role):
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

        cursor.execute(
            "INSERT INTO users (username, email, password, role) VALUES (?, ?, ?, ?)",
            (username, email, hashed_password, role)
        )
        conn.commit()
        success = True
    except sqlite3.IntegrityError:
        success = False
    finally:
        conn.close()
    return success






def get_user(username, password):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT user_id, password, role FROM users WHERE username = ?", (username,))
    user = cursor.fetchone()
    conn.close()

    if user:
        stored_hashed_password = user[1]

        if bcrypt.checkpw(password.encode('utf-8'), stored_hashed_password):
            return (user[0], user[2])
    
    return None




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

def get_comments_for_ticket(ticket_id):
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT comments.comment_id, comments.ticket_id, comments.user_id, comments.message, comments.created_at, users.username
        FROM comments
        JOIN users ON comments.user_id = users.user_id
        WHERE comments.ticket_id = ?
        ORDER BY comments.created_at ASC
    """, (ticket_id,))

    comments = cursor.fetchall()
    conn.close()
    return comments


def delete_ticket(ticket_id):
    conn = get_db_connection()
    cursor = conn.cursor()

    # First delete comments linked to ticket (because of FK constraint)
    cursor.execute("DELETE FROM comments WHERE ticket_id = ?", (ticket_id,))
    
    cursor.execute("DELETE FROM tickets WHERE ticket_id = ?", (ticket_id,))
    conn.commit()
    conn.close()

def update_ticket_status(ticket_id, new_status):
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("UPDATE tickets SET status = ? WHERE ticket_id = ?", (new_status, ticket_id))
    conn.commit()
    conn.close()


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


