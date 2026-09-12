import pytest

import src.audit.pipeline_audit as pipeline_audit


class FakeCursor:
    def __init__(self, fetchone_result=None, execute_error=None):
        self.fetchone_result = fetchone_result
        self.execute_error = execute_error
        self.executed_sql = None
        self.executed_params = None

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        return False

    def execute(self, sql, params):
        if self.execute_error:
            raise self.execute_error

        self.executed_sql = sql
        self.executed_params = params

    def fetchone(self):
        return self.fetchone_result


class FakeConnection:
    def __init__(self, cursor):
        self.cursor_object = cursor
        self.commit_called = False
        self.rollback_called = False
        self.close_called = False

    def cursor(self):
        return self.cursor_object

    def commit(self):
        self.commit_called = True

    def rollback(self):
        self.rollback_called = True

    def close(self):
        self.close_called = True


def test_start_pipeline_run_creates_running_audit_record(monkeypatch):
    cursor = FakeCursor(fetchone_result=(123,))
    connection = FakeConnection(cursor)

    monkeypatch.setattr(
        pipeline_audit,
        "get_connection",
        lambda: connection,
    )

    result = pipeline_audit.start_pipeline_run()

    assert result == 123
    assert connection.commit_called is True
    assert connection.rollback_called is False
    assert connection.close_called is True

    assert cursor.executed_params == (
        pipeline_audit.PIPELINE_NAME,
        "RUNNING",
    )


def test_complete_pipeline_run_marks_run_successful(monkeypatch):
    cursor = FakeCursor()
    connection = FakeConnection(cursor)

    monkeypatch.setattr(
        pipeline_audit,
        "get_connection",
        lambda: connection,
    )

    pipeline_audit.complete_pipeline_run(
        pipeline_run_id=123,
        raw_count=10000,
        valid_count=9960,
        rejected_count=40,
        transformed_count=9960,
        scored_count=9960,
        fact_loaded_count=9960,
        rejected_loaded_count=40,
    )

    assert connection.commit_called is True
    assert connection.rollback_called is False
    assert connection.close_called is True

    assert cursor.executed_params == (
        "SUCCESS",
        10000,
        9960,
        40,
        9960,
        9960,
        9960,
        40,
        123,
    )


def test_fail_pipeline_run_marks_run_failed(monkeypatch):
    cursor = FakeCursor()
    connection = FakeConnection(cursor)

    monkeypatch.setattr(
        pipeline_audit,
        "get_connection",
        lambda: connection,
    )

    pipeline_audit.fail_pipeline_run(
        pipeline_run_id=123,
        error_message="RuntimeError: database unavailable",
    )

    assert connection.commit_called is True
    assert connection.rollback_called is False
    assert connection.close_called is True

    assert cursor.executed_params == (
        "FAILED",
        "RuntimeError: database unavailable",
        123,
    )


def test_start_pipeline_run_rolls_back_on_failure(monkeypatch):
    error = RuntimeError("database unavailable")

    cursor = FakeCursor(execute_error=error)
    connection = FakeConnection(cursor)

    monkeypatch.setattr(
        pipeline_audit,
        "get_connection",
        lambda: connection,
    )

    with pytest.raises(RuntimeError, match="database unavailable"):
        pipeline_audit.start_pipeline_run()

    assert connection.commit_called is False
    assert connection.rollback_called is True
    assert connection.close_called is True


def test_complete_pipeline_run_rolls_back_on_failure(monkeypatch):
    error = RuntimeError("update failed")

    cursor = FakeCursor(execute_error=error)
    connection = FakeConnection(cursor)

    monkeypatch.setattr(
        pipeline_audit,
        "get_connection",
        lambda: connection,
    )

    with pytest.raises(RuntimeError, match="update failed"):
        pipeline_audit.complete_pipeline_run(
            pipeline_run_id=123,
            raw_count=100,
            valid_count=90,
            rejected_count=10,
            transformed_count=90,
            scored_count=90,
            fact_loaded_count=90,
            rejected_loaded_count=10,
        )

    assert connection.commit_called is False
    assert connection.rollback_called is True
    assert connection.close_called is True


def test_fail_pipeline_run_rolls_back_on_failure(monkeypatch):
    error = RuntimeError("audit update failed")

    cursor = FakeCursor(execute_error=error)
    connection = FakeConnection(cursor)

    monkeypatch.setattr(
        pipeline_audit,
        "get_connection",
        lambda: connection,
    )

    with pytest.raises(RuntimeError, match="audit update failed"):
        pipeline_audit.fail_pipeline_run(
            pipeline_run_id=123,
            error_message="original pipeline error",
        )

    assert connection.commit_called is False
    assert connection.rollback_called is True
    assert connection.close_called is True