import pytest
from audit.logger import AuditLogger
import os

def test_log_insertion(logger):
    """Verifica que un log se inserta correctamente en la BD."""
    log_id = logger.log("CREATE", "/vol/data", "success", user="uriel")

    cursor = logger.conn.execute("SELECT * FROM audit_log")
    logs = cursor.fetchall()

    assert len(logs) == 1
    log = dict(logs[0])
    assert log["operation"] == "CREATE"
    assert log["path"] == "/vol/data"
    assert log["status"] == "success"
    assert log["user"] == "uriel"
    assert log["message"] is None
    assert log_id == 1


def test_log_returns_id(logger):
    """Verifica que log() retorna el ID del registro insertado."""
    id1 = logger.log("CREATE", "/vol/a", "success")
    id2 = logger.log("READ",   "/vol/b", "success")

    assert id1 == 1
    assert id2 == 2


def test_log_multiple_records(logger):
    """Verifica que múltiples logs se guardan correctamente."""
    logger.log("CREATE", "/vol/data", "success", user="uriel")
    logger.log("READ",   "/vol/data", "success", user="uriel")
    logger.log("DELETE", "/vol/data", "failed",  user="admin")

    assert logger.count_logs() == 3


def test_get_logs_filter_by_status(logger_with_logs):
    """Verifica filtrado por status."""
    failed = logger_with_logs.get_logs(status="failed")

    assert len(failed) == 1
    assert failed[0]["status"] == "failed"
    assert failed[0]["user"] == "admin"
    assert failed[0]["message"] == "Permission denied"


def test_get_logs_filter_by_operation(logger_with_logs):
    """Verifica filtrado por operation."""
    creates = logger_with_logs.get_logs(operation="CREATE")

    assert len(creates) == 1
    assert creates[0]["operation"] == "CREATE"


def test_get_logs_all(logger_with_logs):
    """Verifica que get_logs() sin filtros retorna todos."""
    logs = logger_with_logs.get_logs()

    assert len(logs) == 3


def test_log_empty_operation_raises_error(logger):
    """Verifica que campos vacíos lanzan ValueError."""
    with pytest.raises(ValueError):
        logger.log("", "/vol/data", "success")


def test_log_empty_path_raises_error(logger):
    """Verifica que path vacío lanza ValueError."""
    with pytest.raises(ValueError):
        logger.log("CREATE", "", "success")


def test_count_logs_by_status(logger_with_logs):
    """Verifica conteo filtrado por status."""
    assert logger_with_logs.count_logs(status="success") == 2
    assert logger_with_logs.count_logs(status="failed") == 1
    assert logger_with_logs.count_logs() == 3


def test_get_connection_creates_file(tmp_path):
    """Verifica que get_connection() crea el archivo de BD correctamente."""
    from audit.db import get_connection, setup_database

    db_path = str(tmp_path / "test.db")
    conn = get_connection(db_path)
    setup_database(conn)

    assert os.path.exists(db_path)
    conn.close()