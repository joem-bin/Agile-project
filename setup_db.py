import sqlite3
import os

DB_NAME = "test.db"

# Remove existing database file if it exists
if os.path.exists(DB_NAME):
    os.remove(DB_NAME)
    print("Database reset.")

# Recreate the database and table
conn = sqlite3.connect(DB_NAME)
cursor = conn.cursor()

cursor.execute("""
    CREATE TABLE items (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL
    )
""")

# Insert sample data
sample_items = [("Item A",), ("Item B",), ("Item C",), ("Item D",), ("Item E",),
                ("Item F",), ("Item G",), ("Item H",), ("Item I",), ("Item J",)]

cursor.executemany("INSERT INTO items (name) VALUES (?)", sample_items)

conn.commit()
conn.close()

print("Database created and populated successfully!")
