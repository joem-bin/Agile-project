import sqlite3
from datetime import datetime



DB_NAME = "test.db"

# works
def fetch_all():
    """Retrieve all records."""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM tickets")
    records = cursor.fetchall()
    conn.close()
    return records

# works
def insert_test_ticket():
    user_id = 1
    title = 'Test Ticket'
    description = 'This is a test ticket inserted by test function.'
    category_id = 1  
    status = 'in progress'
    created_at = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO tickets (user_id, category_id, title, description, status, created_at)
        VALUES (?, ?, ?, ?, ?, ?)
    """, (user_id, category_id, title, description, status, created_at))

    conn.commit()
    conn.close()

    print(f"Inserted test ticket for user_id {user_id} with status '{status}'.")


if __name__ == "__main__":
    insert_test_ticket()

