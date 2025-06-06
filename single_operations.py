import sqlite3

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

# need updating
def insert_item(name):
    """Insert a new item."""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("INSERT INTO items (name) VALUES (?)", (name,))
    conn.commit()
    conn.close()
    print(f"Inserted: {name}")

# need updating
def update_item(item_id, new_name):
    """Update an existing item."""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("UPDATE items SET name = ? WHERE id = ?", (new_name, item_id))
    conn.commit()
    conn.close()
    print(f"Updated item {item_id} to {new_name}")

# need updating
def delete_item(item_id):
    """Delete an item."""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("DELETE FROM items WHERE id = ?", (item_id,))
    conn.commit()
    conn.close()
    print(f"Deleted item {item_id}")

if __name__ == "__main__":
    print("Current records:", fetch_all())

