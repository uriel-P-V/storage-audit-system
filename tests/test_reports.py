import pytest


def test_summary(reporter_with_logs):
    """Verifica el resumen total de operaciones."""
    result = reporter_with_logs.summary()

    assert result["total"] == 5
    assert result["successful"] == 2
    assert result["failed"] == 3
    assert "CREATE" in result["by_operation"]


def test_failed_operations(reporter_with_logs):
    """Verifica que solo retorna operaciones fallidas."""
    failed = reporter_with_logs.failed_operations()

    assert len(failed) == 3
    for op in failed:
        assert op["status"] == "failed"


def test_top_paths(reporter_with_logs):
    """Verifica que retorna el path con más fallos primero."""
    top = reporter_with_logs.top_paths()

    assert top[0]["path"] == "/vol/backup"
    assert top[0]["failures"] == 2


def test_user_activity(reporter_with_logs):
    """Verifica el resumen de actividad de un usuario."""
    activity = reporter_with_logs.user_activity("uriel")

    assert activity["user"] == "uriel"
    assert activity["total"] == 3
    assert activity["successful"] == 2
    assert activity["failed"] == 1
