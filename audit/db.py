"""
db.py
-----
Handles SQLite database connection and schema setup
for the storage audit system.
"""

import sqlite3
import os


DB_PATH = os.environ.get("DB_PATH", "audit.db")


def get_connection(db_path: str = DB_PATH) -> sqlite3.Connection:
    """
    Create and return a SQLite database connection.
    
    Args:
        db_path: Path to the SQLite file. 
                 Use ":memory:" for in-memory DB (tests)
    """
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row  # allows dict-like access to rows
    return conn


def setup_database(conn: sqlite3.Connection) -> None:
    """
    Create tables if they don't exist.
    
    Tables:
        audit_log — records every storage operation
    """
    conn.execute("""
        CREATE TABLE IF NOT EXISTS audit_log (
            id        INTEGER PRIMARY KEY AUTOINCREMENT,
            operation TEXT NOT NULL,
            path      TEXT NOT NULL,
            status    TEXT NOT NULL,
            user      TEXT NOT NULL DEFAULT 'system',
            message   TEXT,
            timestamp REAL NOT NULL
        )
    """)
    conn.commit()