import sqlite3
import os
from datetime import datetime

DATABASE_PATH = os.getenv('DATABASE_PATH', 'users.db')

def init_db():
    """Initialize the database with required tables."""
    conn = sqlite3.connect(DATABASE_PATH)
    cursor = conn.cursor()
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            email TEXT UNIQUE NOT NULL,
            lichess_username TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            last_newsletter_sent TIMESTAMP
        )
    ''')
    
    conn.commit()
    conn.close()

def add_user(email, lichess_username):
    """Add a new user to the database."""
    conn = sqlite3.connect(DATABASE_PATH)
    cursor = conn.cursor()
    
    try:
        cursor.execute(
            'INSERT INTO users (email, lichess_username) VALUES (?, ?)',
            (email, lichess_username)
        )
        conn.commit()
        return True, "User registered successfully"
    except sqlite3.IntegrityError:
        return False, "Email already registered"
    finally:
        conn.close()

def get_all_users():
    """Get all users from the database."""
    conn = sqlite3.connect(DATABASE_PATH)
    cursor = conn.cursor()
    
    cursor.execute('SELECT id, email, lichess_username, last_newsletter_sent FROM users')
    users = cursor.fetchall()
    conn.close()
    
    return [
        {
            'id': user[0],
            'email': user[1],
            'lichess_username': user[2],
            'last_newsletter_sent': user[3]
        }
        for user in users
    ]

def update_newsletter_sent(user_id):
    """Update the last newsletter sent timestamp for a user."""
    conn = sqlite3.connect(DATABASE_PATH)
    cursor = conn.cursor()
    
    cursor.execute(
        'UPDATE users SET last_newsletter_sent = ? WHERE id = ?',
        (datetime.now().isoformat(), user_id)
    )
    conn.commit()
    conn.close()
