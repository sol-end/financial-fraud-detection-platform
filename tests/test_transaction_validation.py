import pandas as pd

from src.validation.transaction_validator import validate_transactions


def test_valid_transaction_passes_validation():
    df = pd.DataFrame(
        [
            {
                "transaction_id": "TEST_VALID",
                "customer_id": "CUST001",
                "transaction_date": "2026-08-01",
                "amount": 100.00,
                "currency": "USD",
                "country": "United States",
            }
        ]
    )

    valid_df, rejected_df = validate_transactions(df)

    assert len(valid_df) == 1
    assert len(rejected_df) == 0


def test_invalid_amount_is_rejected():
    df = pd.DataFrame(
        [
            {
                "transaction_id": "TEST_INVALID_AMOUNT",
                "customer_id": "CUST001",
                "transaction_date": "2026-08-01",
                "amount": -10.00,
                "currency": "USD",
                "country": "United States",
            }
        ]
    )

    valid_df, rejected_df = validate_transactions(df)

    assert len(valid_df) == 0
    assert len(rejected_df) == 1
    assert rejected_df.iloc[0]["rejection_reason"] == "INVALID_AMOUNT"


def test_multiple_validation_failures_are_all_recorded():
    df = pd.DataFrame(
        [
            {
                "transaction_id": "TEST_MULTI_FAILURE",
                "customer_id": None,
                "transaction_date": "not-a-date",
                "amount": -10.00,
                "currency": "XYZ",
                "country": "United States",
            }
        ]
    )

    valid_df, rejected_df = validate_transactions(df)

    assert len(valid_df) == 0
    assert len(rejected_df) == 1

    rejection_reason = rejected_df.iloc[0]["rejection_reason"]

    assert "MISSING_CUSTOMER_ID" in rejection_reason
    assert "INVALID_AMOUNT" in rejection_reason
    assert "INVALID_CURRENCY" in rejection_reason
    assert "INVALID_TRANSACTION_DATE" in rejection_reason

 
def test_duplicate_transaction_id_is_rejected():
    test_data = pd.DataFrame(
        [
            {
                "transaction_id": "TXN_DUPLICATE_001",
                "customer_id": "CUST001",
                "transaction_date": "2026-08-01",
                "amount": 100.00,
                "currency": "USD",
                "country": "United States",
            },
            {
                "transaction_id": "TXN_DUPLICATE_001",
                "customer_id": "CUST002",
                "transaction_date": "2026-08-02",
                "amount": 200.00,
                "currency": "USD",
                "country": "United States",
            },
        ]
    )

    valid_df, rejected_df = validate_transactions(test_data)

    assert len(valid_df) == 1
    assert len(rejected_df) == 1

    assert rejected_df.iloc[0]["rejection_reason"] == (
        "DUPLICATE_TRANSACTION_ID"
    )
