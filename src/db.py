import sqlite3
import os
from dotenv import load_dotenv

load_dotenv()

DB_PATH = os.getenv('DB_PATH', '../freelance.db')

def get_connection():
    return sqlite3.connect(DB_PATH)

def init_db():
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS projects (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                client TEXT NOT NULL,
                category TEXT NOT NULL,
                rate REAL NOT NULL,
                payment_type TEXT CHECK(payment_type IN ('fixed', 'hourly')) NOT NULL,
                start_date TEXT NOT NULL,
                deadline TEXT NOT NULL,
                status TEXT CHECK(status IN ('waiting', 'in_progress', 'review', 'completed', 'cancelled')) NOT NULL,
                hours_worked REAL DEFAULT 0,
                total_amount REAL NOT NULL,
                paid BOOLEAN DEFAULT 0,
                paid_date TEXT
            )
        ''')
        print("✓ Таблица projects создана (или уже существует)")

if __name__ == '__main__':
    init_db()