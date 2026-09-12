import pandas as pd
import pytest

import src.loading.transaction_loader as transaction_loader


def create_valid_transaction():
    return pd.DataFrame(
        [
            {
                "transaction_id": "TXN_TEST_001",
                "customer_id": "CUST001",
                "transaction_date": pd.Timestamp("2026-08-01 10:00:00"),
                "amount": 125.50,
                "currency": "USD",
                "merchant_id": "MERCH001",
                "merchant_category": "Retail",
                "payment_method": "Credit Card",
                "country": "United States",
                "device_id": "DEV001",
                "ip_address": "192.168.1.10",
                "fraud_score": 0.0,
                "fraud_flag": False,
                "fraud_reason": None,
                "risk_decision": "APPROVE",
            }
        ]
    )


class FakeCursor:
    def __init__(self, execute_error=None, rowcount=1):
        self.execute_error = execute_error
        self.rowcount = rowcount
        self.executed_rows = []

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        return False

    def execute(self, sql, params):
        if self.execute_error:
            raise self.execute_error

        self.executed_rows.append(params)


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


def test_loader_rejects_missing_required_columns():
    test_data = create_valid_transaction()

    test_data = test_data.drop(columns=["amount"])

    with pytest.raises(ValueError, match="Missing required columns"):
        transaction_loader.load_fact_transactions(test_data)


def test_valid_transaction_is_loaded_into_fact_table():
    test_data = create_valid_transaction()

    test_data.loc[0, "transaction_id"] = "TXN_TEST_LOADER_001"

    loaded_count = transaction_loader.load_fact_transactions(test_data)

    assert loaded_count == 1


def test_rejected_loader_rejects_missing_required_columns():
    test_data = pd.DataFrame(
        [
            {
                "transaction_id": "TXN_REJECT_TEST_001",
                "source_file": "test_file.csv",
            }
        ]
    )

    with pytest.raises(ValueError, match="Missing required columns"):
        transaction_loader.load_rejected_transactions(test_data)


def test_rejected_transaction_loader_is_idempotent():
    test_data = pd.DataFrame(
        [
            {
                "transaction_id": "TXN_TEST_REJECT_001",
                "source_file": "test_rejected_transactions.csv",
                "rejection_reason": "Invalid amount",
            }
        ]
    )

    first_load_count = transaction_loader.load_rejected_transactions(
        test_data
    )
    second_load_count = transaction_loader.load_rejected_transactions(
        test_data
    )

    assert first_load_count in (0, 1)
    assert second_load_count == 0


def test_fact_loader_rolls_back_on_database_failure(monkeypatch):
    error = RuntimeError("database insert failed")

    cursor = FakeCursor(execute_error=error)
    connection = FakeConnection(cursor)

    monkeypatch.setattr(
        transaction_loader,
        "get_connection",
        lambda: connection,
    )

    test_data = create_valid_transaction()

    with pytest.raises(RuntimeError, match="database insert failed"):
        transaction_loader.load_fact_transactions(test_data)

    assert connection.commit_called is False
    assert connection.rollback_called is True
    assert connection.close_called is True


def test_rejected_transaction_loader_counts_new_insert(monkeypatch):
    cursor = FakeCursor(rowcount=1)
    connection = FakeConnection(cursor)

    monkeypatch.setattr(
        transaction_loader,
        "get_connection",
        lambda: connection,
    )

    test_data = pd.DataFrame(
        [
            {
                "transaction_id": "TXN_NEW_REJECT_001",
                "source_file": "test_file.csv",
                "rejection_reason": "Invalid amount",
            }
        ]
    )

    result = transaction_loader.load_rejected_transactions(test_data)

    assert result == 1
    assert connection.commit_called is True
    assert connection.rollback_called is False
    assert connection.close_called is True


def test_rejected_transaction_loader_rolls_back_on_database_failure(
    monkeypatch,
):
    error = RuntimeError("rejected transaction insert failed")

    cursor = FakeCursor(execute_error=error)
    connection = FakeConnection(cursor)

    monkeypatch.setattr(
        transaction_loader,
        "get_connection",
        lambda: connection,
    )

    test_data = pd.DataFrame(
        [
            {
                "transaction_id": "TXN_REJECT_FAILURE_001",
                "source_file": "test_file.csv",
                "rejection_reason": "Invalid amount",
            }
        ]
    )

    with pytest.raises(
        RuntimeError,
        match="rejected transaction insert failed",
    ):
        transaction_loader.load_rejected_transactions(test_data)

    assert connection.commit_called is False
    assert connection.rollback_called is True
    assert connection.close_called is True
