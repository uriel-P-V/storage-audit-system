"""
reports.py
----------
Generates audit reports from the storage operation logs.
Used by QA teams to identify failures, track operations,
and prioritize fixes.
"""

import sqlite3
from .db import get_connection, setup_database


class AuditReporter:

    def __init__(self, conn: sqlite3.Connection = None):
        self.conn = conn or get_connection()
        setup_database(self.conn)

    def summary(self) -> dict:
        """
        Returns a summary of all operations.

        Returns:
            dict with total counts by operation type and status
        """
        cursor = self.conn.execute("""
            SELECT 
                COUNT(*)                                    as total,
                SUM(CASE WHEN status='success' THEN 1 END) as successful,
                SUM(CASE WHEN status='failed'  THEN 1 END) as failed
            FROM audit_log
        """)
        row = dict(cursor.fetchone())

        cursor = self.conn.execute("""
            SELECT operation, COUNT(*) as count
            FROM audit_log
            GROUP BY operation
            ORDER BY count DESC
        """)
        by_operation = {row["operation"]: row["count"] 
                       for row in cursor.fetchall()}

        return {
            "total":        row["total"] or 0,
            "successful":   row["successful"] or 0,
            "failed":       row["failed"] or 0,
            "by_operation": by_operation
        }

    def failed_operations(self, limit: int = 10) -> list:
        """
        Returns failed operations ordered by most recent.

        Args:
            limit: Maximum number of records to return

        Returns:
            List of failed log records
        """
        cursor = self.conn.execute("""
            SELECT * FROM audit_log
            WHERE status = 'failed'
            ORDER BY timestamp DESC
            LIMIT ?
        """, (limit,))
        return [dict(row) for row in cursor.fetchall()]

    def top_paths(self, limit: int = 5) -> list:
        """
        Returns paths with most failures — helps prioritize fixes.

        Args:
            limit: Number of top paths to return

        Returns:
            List of dicts with path and failure count
        """
        cursor = self.conn.execute("""
            SELECT path, COUNT(*) as failures
            FROM audit_log
            WHERE status = 'failed'
            GROUP BY path
            ORDER BY failures DESC
            LIMIT ?
        """, (limit,))
        return [dict(row) for row in cursor.fetchall()]

    def user_activity(self, user: str) -> dict:
        """
        Returns activity summary for a specific user.

        Args:
            user: Username to query

        Returns:
            dict with user's operation counts
        """
        cursor = self.conn.execute("""
            SELECT 
                COUNT(*)                                    as total,
                SUM(CASE WHEN status='success' THEN 1 END) as successful,
                SUM(CASE WHEN status='failed'  THEN 1 END) as failed
            FROM audit_log
            WHERE user = ?
        """, (user,))
        row = dict(cursor.fetchone())
        return {
            "user":       user,
            "total":      row["total"] or 0,
            "successful": row["successful"] or 0,
            "failed":     row["failed"] or 0,
        }