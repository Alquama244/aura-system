import sqlite3
import json
from datetime import datetime

DB_NAME = "aura_inventory.db"

def init_db():
    """Initializes the SQLite database and creates the scans table if it doesn't exist."""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS scans (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp TEXT,
            object_counts TEXT,
            ai_analysis TEXT
        )
    """)
    conn.commit()
    conn.close()

def save_scan(object_counts, ai_analysis):
    """Saves a new inventory scan record to the SQLite database."""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    cursor.execute("""
        INSERT INTO scans (timestamp, object_counts, ai_analysis)
        VALUES (?, ?, ?)
    """, (timestamp, json.dumps(object_counts), ai_analysis))
    scan_id = cursor.lastrowid
    conn.commit()
    conn.close()
    return scan_id
