import sqlite3

DB_NAME = "test.db"

def fetch_all():
    """Retrieve all records."""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM items")
    records = cursor.fetchall()
    conn.close()
    return records

def insert_item(name):
    """Insert a new item."""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("INSERT INTO items (name) VALUES (?)", (name,))
    conn.commit()
    conn.close()
    print(f"Inserted: {name}")

def update_item(item_id, new_name):
    """Update an existing item."""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("UPDATE items SET name = ? WHERE id = ?", (new_name, item_id))
    conn.commit()
    conn.close()
    print(f"Updated item {item_id} to {new_name}")

def delete_item(item_id):
    """Delete an item."""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("DELETE FROM items WHERE id = ?", (item_id,))
    conn.commit()
    conn.close()
    print(f"Deleted item {item_id}")

if __name__ == "__main__":
    # Test fetching all records
    print("Current records:", fetch_all())

    # Example operations
    insert_item("New Item")
    update_item(1, "Updated Item A")
    delete_item(2)
    
    print("Updated records:", fetch_all())
