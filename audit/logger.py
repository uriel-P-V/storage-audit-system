"""
logger.py
---------
Records storage operations into the audit database.
Every create, read, and delete operation is logged
with its result and timestamp.
"""

import time
import sqlite3
from .db import get_connection, setup_database


class AuditLogger:

    def __init__(self, conn: sqlite3.Connection = None):
        """
        Args:
            conn: SQLite connection. If None, creates a new one.
                  Pass ":memory:" connection for tests.
        """
        self.conn = conn or get_connection()
        setup_database(self.conn)

    def log(self, operation: str, path: str, status: str,
            user: str = "system", message: str = None) -> int:
        """
        Record a storage operation in the audit log.

        Args:
            operation: Type of operation (CREATE, READ, DELETE, WRITE)
            path:      Target path or volume
            status:    Result (success, failed)
            user:      Who performed the operation
            message:   Optional details or error message

        Returns:
            ID of the inserted record
        """
        if not operation or not path or not status:
            raise ValueError("operation, path and status are required")

        cursor = self.conn.execute(
            """
            INSERT INTO audit_log (operation, path, status, user, message, timestamp)
            VALUES (?, ?, ?, ?, ?, ?)
            """,
            (operation, path, status, user, message, time.time())
        )
        self.conn.commit()
        return cursor.lastrowid

    def get_logs(self, operation: str = None, status: str = None) -> list:
        """
        Retrieve audit logs with optional filters.

        Args:
            operation: Filter by operation type
            status:    Filter by status

        Returns:
            List of log records as dictionaries
        """
        query = "SELECT * FROM audit_log WHERE 1=1"
        params = []

        if operation:
            query += " AND operation = ?"
            params.append(operation)

        if status:
            query += " AND status = ?"
            params.append(status)

        query += " ORDER BY timestamp DESC"

        cursor = self.conn.execute(query, params)
        return [dict(row) for row in cursor.fetchall()]

    def count_logs(self, status: str = None) -> int:
        """Count total logs, optionally filtered by status."""
        if status:
            cursor = self.conn.execute(
                "SELECT COUNT(*) FROM audit_log WHERE status = ?", (status,)
            )
        else:
            cursor = self.conn.execute("SELECT COUNT(*) FROM audit_log")
        return cursor.fetchone()[0]