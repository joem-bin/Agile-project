import sqlite3
import bcrypt
import os
from dotenv import load_dotenv


load_dotenv()
DB_NAME = os.getenv("DB_NAME")

def reset_database():
    """Deletes the existing database file if it exists."""
    if os.path.exists(DB_NAME):
        os.remove(DB_NAME)
        print("Database reset.")

def create_tables():
    """Creates the database and all required tables."""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    # Users Table
    cursor.execute("""
        CREATE TABLE users (
            user_id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL UNIQUE,
            email TEXT NOT NULL UNIQUE,
            password BLOB NOT NULL,
            role TEXT NOT NULL
        )
    """)

    # Categories Table
    cursor.execute("""
        CREATE TABLE categories (
            category_id INTEGER PRIMARY KEY AUTOINCREMENT,
            category_name TEXT NOT NULL UNIQUE
        )
    """)

    # Tickets Table
    cursor.execute("""
        CREATE TABLE tickets (
            ticket_id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            category_id INTEGER NOT NULL,
            title TEXT NOT NULL,
            description TEXT NOT NULL,
            status TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users(user_id),
            FOREIGN KEY (category_id) REFERENCES categories(category_id)
        )
    """)

    # Comments Table
    cursor.execute("""
        CREATE TABLE comments (
            comment_id INTEGER PRIMARY KEY AUTOINCREMENT,
            ticket_id INTEGER NOT NULL,
            user_id INTEGER NOT NULL,
            message TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (ticket_id) REFERENCES tickets(ticket_id),
            FOREIGN KEY (user_id) REFERENCES users(user_id)
        )
    """)

    conn.commit()
    conn.close()
    print("Database tables created successfully.")

def insert_sample_data():
    """Inserts sample data into the database."""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    def hash_password(password_str):
        return bcrypt.hashpw(password_str.encode('utf-8'), bcrypt.gensalt())

    sample_users = [
        ("admin1", "admin1@example.com", hash_password("adminpass1"), "admin"),
        ("admin2", "admin2@example.com", hash_password("adminpass2"), "admin"),
        ("user1", "user1@example.com", hash_password("userpass1"), "user"),
        ("user2", "user2@example.com", hash_password("userpass2"), "user"),
        ("user3", "user3@example.com", hash_password("userpass3"), "user"),
        ("user4", "user4@example.com", hash_password("userpass4"), "user"),
        ("user5", "user5@example.com", hash_password("userpass5"), "user"),
        ("user6", "user6@example.com", hash_password("userpass6"), "user"),
        ("user7", "user7@example.com", hash_password("userpass7"), "user"),
        ("user8", "user8@example.com", hash_password("userpass8"), "user"),
    ]
    cursor.executemany("INSERT INTO users (username, email, password, role) VALUES (?, ?, ?, ?)", sample_users)

    sample_categories = [
        ("Software Issue",), ("Hardware Issue",), ("Access Request",), ("Network Issue",), ("Security Issue",),
        ("UI Bug",), ("Performance Issue",), ("Database Error",), ("API Failure",), ("Other",)
    ]
    cursor.executemany("INSERT INTO categories (category_name) VALUES (?)", sample_categories)

    sample_tickets = [
        (1, 1, "Can't install software", "Installation fails with error code", "open"),
        (2, 2, "Computer won't boot", "Stuck on startup screen", "open"),
        (3, 3, "Need VPN access", "Can't connect remotely", "in progress"),
        (4, 4, "Slow network", "Internet keeps dropping", "resolved"),
        (5, 5, "Suspicious email", "Possible phishing attack", "open"),
        (6, 6, "Button misalignment", "UI not displaying correctly", "in progress"),
        (7, 7, "App crashing", "Memory leak suspected", "open"),
        (8, 8, "Database connection issue", "Server not responding", "closed"),
        (9, 9, "API timeout", "3rd party service unresponsive", "resolved"),
        (10, 10, "General support request", "Need help with configuration", "open"),
    ]
    cursor.executemany("INSERT INTO tickets (user_id, category_id, title, description, status) VALUES (?, ?, ?, ?, ?)", sample_tickets)

    sample_comments = [
        (1, 1, "Have you tried rebooting?"),
        (2, 2, "Check your startup settings."),
        (3, 3, "VPN config updated, please retry."),
        (4, 4, "Network issues seem resolved now."),
        (5, 5, "Marking as phishing, IT should investigate."),
        (6, 6, "Working on a UI fix."),
        (7, 7, "Checking logs for memory leaks."),
        (8, 8, "Database restored, retry connection."),
        (9, 9, "API provider confirmed downtime."),
        (10, 10, "Assistance provided, closing ticket."),
    ]
    cursor.executemany("INSERT INTO comments (ticket_id, user_id, message) VALUES (?, ?, ?)", sample_comments)

    conn.commit()
    conn.close()
    print("Database populated successfully.")

if __name__ == "__main__":
    reset_database()
    create_tables()
    insert_sample_data()
