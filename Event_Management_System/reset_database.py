#!/usr/bin/env python3
"""
Database reset script for Event Management System
This will delete the old database and create a fresh one
"""

import os
import sqlite3

def reset_database():
    """Reset the database with proper schema"""
    
    # Remove old database if it exists
    if os.path.exists('event.db'):
        os.remove('event.db')
        print("🗑️  Removed old database")
    
    # Create new database with proper schema
    conn = sqlite3.connect('event.db')
    
    # Users table with email column
    conn.execute("""
    CREATE TABLE users(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT UNIQUE NOT NULL,
        password TEXT NOT NULL,
        email TEXT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )""")
    
    # Bookings table
    conn.execute("""
    CREATE TABLE bookings(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT NOT NULL,
        event_type TEXT NOT NULL,
        date TEXT NOT NULL,
        guests INTEGER NOT NULL,
        status TEXT DEFAULT 'pending',
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )""")
    
    # Chats table
    conn.execute("""
    CREATE TABLE chats(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_message TEXT NOT NULL,
        bot_reply TEXT NOT NULL,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )""")
    
    # Events table
    conn.execute("""
    CREATE TABLE events(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        description TEXT,
        price DECIMAL(10,2) NOT NULL,
        category TEXT NOT NULL,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )""")
    
    # Insert default events
    default_events = [
        ('Wedding Package', 'Complete wedding planning with decoration, catering, and photography', 50000.00, 'Wedding'),
        ('Birthday Celebration', 'Birthday party setup with cake, decorations, and entertainment', 20000.00, 'Birthday'),
        ('Corporate Event', 'Professional corporate event management with AV setup', 40000.00, 'Corporate'),
        ('Anniversary Special', 'Romantic anniversary celebration setup', 30000.00, 'Anniversary'),
        ('Baby Shower', 'Beautiful baby shower arrangement with themed decorations', 25000.00, 'Baby Shower')
    ]
    
    conn.executemany("INSERT INTO events (name, description, price, category) VALUES (?, ?, ?, ?)", default_events)
    
    conn.commit()
    conn.close()
    
    print("✅ Created fresh database with proper schema")
    print("✅ Added default events")
    print("🚀 You can now run: python app.py")

if __name__ == "__main__":
    print("🔄 Resetting Event Management Database...")
    reset_database()
    print("✅ Database reset complete!")