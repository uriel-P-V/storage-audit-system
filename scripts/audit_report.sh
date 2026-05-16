#!/bin/bash
# audit_report.sh
# ---------------
# Queries the audit database and displays a report in the terminal.
#
# Usage:
#   ./scripts/audit_report.sh
#   DB_PATH=custom.db ./scripts/audit_report.sh

DB_PATH=${DB_PATH:-"audit.db"}

echo "========================================"
echo "  Storage Audit Report"
echo "  DB: $DB_PATH"
echo "========================================"

# Check if DB exists
if [ ! -f "$DB_PATH" ]; then
    echo "ERROR: Database not found: $DB_PATH"
    echo "Run ./scripts/setup_db.sh first"
    exit 1
fi

python - << EOF
import sqlite3
import os

db_path = "$DB_PATH"
conn = sqlite3.connect(db_path)
conn.row_factory = sqlite3.Row

# Summary
cursor = conn.execute("""
    SELECT 
        COUNT(*) as total,
        SUM(CASE WHEN status='success' THEN 1 END) as successful,
        SUM(CASE WHEN status='failed'  THEN 1 END) as failed
    FROM audit_log
""")
row = dict(cursor.fetchone())
total      = row["total"] or 0
successful = row["successful"] or 0
failed     = row["failed"] or 0

print(f"\n  Total operations : {total}")
print(f"  Successful       : {successful}")
print(f"  Failed           : {failed}")

if total > 0:
    pass_rate = round((successful / total) * 100, 1)
    print(f"  Pass rate        : {pass_rate}%")

# Failed operations
if failed > 0:
    print("\n  --- Recent Failures ---")
    cursor = conn.execute("""
        SELECT operation, path, user, message
        FROM audit_log
        WHERE status = 'failed'
        ORDER BY timestamp DESC
        LIMIT 5
    """)
    for row in cursor.fetchall():
        print(f"  [{row['operation']}] {row['path']} by {row['user']} — {row['message']}")

# Top paths with failures
print("\n  --- Top Paths with Failures ---")
cursor = conn.execute("""
    SELECT path, COUNT(*) as failures
    FROM audit_log
    WHERE status = 'failed'
    GROUP BY path
    ORDER BY failures DESC
    LIMIT 3
""")
rows = cursor.fetchall()
if rows:
    for row in rows:
        print(f"  {row['path']} — {row['failures']} failure(s)")
else:
    print("  No failures found")

print()
conn.close()
EOF

echo "========================================"
exit 0