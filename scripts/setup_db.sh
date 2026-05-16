#!/bin/bash
# setup_db.sh
# -----------
# Initializes the SQLite audit database.
# Safe to run multiple times — won't overwrite existing data.
#
# Usage:
#   ./scripts/setup_db.sh
#   DB_PATH=custom.db ./scripts/setup_db.sh

DB_PATH=${DB_PATH:-"audit.db"}

echo "========================================"
echo "  Storage Audit System — DB Setup"
echo "  DB Path: $DB_PATH"
echo "========================================"

# Check if Python is available
if ! command -v python &> /dev/null; then
    echo "ERROR: Python not found"
    exit 1
fi

# Initialize database using Python module
python - << EOF
import sqlite3
import os

db_path = "$DB_PATH"
conn = sqlite3.connect(db_path)
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
conn.close()
print(f"  Database initialized: {db_path}")
EOF

if [ $? -eq 0 ]; then
    echo "  Status: SUCCESS"
    echo "========================================"
    exit 0
else
    echo "  Status: FAILED"
    echo "========================================"
    exit 1
fi