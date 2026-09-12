import pandas as pd

from src.transformation.transaction_transformer import (
    transform_transactions,
)


def main():
    test_data = pd.DataFrame(
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

    transformed_df = transform_transactions(test_data)

    print("=== TRANSFORMATION TEST RESULTS ===")
    print()

    print("DATA TYPES:")
    print(transformed_df.dtypes.to_string())

    print()
    print("TRANSFORMED RECORD:")
    print(transformed_df.to_string(index=False))


if __name__ == "__main__":
    main()