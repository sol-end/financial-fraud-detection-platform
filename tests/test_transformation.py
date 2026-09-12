import pandas as pd

from src.transformation.transaction_transformer import (
    transform_transactions,
)


def create_test_data():
    return pd.DataFrame(
        [
            {
                "transaction_id": " TXN_TEST_001 ",
                "customer_id": " CUST001 ",
                "transaction_date": "2026-08-01 10:00:00",
                "amount": "125.50",
                "currency": " USD ",
                "merchant_id": " MERCH001 ",
                "merchant_category": " Retail ",
                "payment_method": " Credit Card ",
                "country": " United States ",
                "device_id": " DEV001 ",
                "ip_address": " 192.168.1.10 ",
            }
        ]
    )


def test_text_fields_are_stripped():
    transformed_df = transform_transactions(create_test_data())

    assert transformed_df.loc[0, "transaction_id"] == "TXN_TEST_001"
    assert transformed_df.loc[0, "customer_id"] == "CUST001"
    assert transformed_df.loc[0, "currency"] == "USD"
    assert transformed_df.loc[0, "merchant_category"] == "Retail"
    assert transformed_df.loc[0, "country"] == "United States"


def test_transaction_date_is_converted_to_datetime():
    transformed_df = transform_transactions(create_test_data())

    assert pd.api.types.is_datetime64_any_dtype(
        transformed_df["transaction_date"]
    )


def test_amount_is_converted_to_numeric():
    transformed_df = transform_transactions(create_test_data())

    assert pd.api.types.is_numeric_dtype(
        transformed_df["amount"]
    )
    assert transformed_df.loc[0, "amount"] == 125.50
