import sqlite3
import os
from pathlib import Path

def init_database():
    """Initialize the SQLite database with schema"""
    PROJECT_ROOT = Path(__file__).parent
    DB_PATH = os.path.join(PROJECT_ROOT, "employees.db")
    
    conn = sqlite3.connect(DB_PATH)
    
    # Create employees table
    conn.execute('''
        CREATE TABLE IF NOT EXISTS employees (
            emp_id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            department TEXT,
            base_salary REAL NOT NULL
        )
    ''')
    
    # Create payroll table
    conn.execute('''
        CREATE TABLE IF NOT EXISTS payroll (
            payroll_id INTEGER PRIMARY KEY AUTOINCREMENT,
            emp_id INTEGER,
            month TEXT,
            deductions REAL,
            net_salary REAL,
            FOREIGN KEY(emp_id) REFERENCES employees(emp_id)
        )
    ''')
    
    conn.commit()
    conn.close()
    print(f"Database initialized at: {DB_PATH}")

if __name__ == "__main__":
    init_database()