import pytest
import sqlite3
from audit.db import setup_database
from audit.logger import AuditLogger


@pytest.fixture
def db_conn():
    """
    In-memory SQLite connection for each test.
    Automatically closed after each test.
    """
    conn = sqlite3.connect(":memory:")
    conn.row_factory = sqlite3.Row
    setup_database(conn)
    yield conn
    conn.close()


@pytest.fixture
def logger(db_conn):
    """AuditLogger using in-memory database."""
    return AuditLogger(conn=db_conn)


@pytest.fixture
def logger_with_logs(logger):
    """AuditLogger with pre-inserted logs for query tests."""
    logger.log("CREATE", "/vol/data", "success", user="uriel")
    logger.log("READ",   "/vol/data", "success", user="uriel")
    logger.log("DELETE", "/vol/data", "failed",  user="admin", message="Permission denied")
    return logger