import pandas as pd

from src.validation.transaction_validator import validate_transactions


def main():
    test_data = pd.DataFrame(
        [
            {
                "transaction_id": "TXN_TEST_001",
                "customer_id": "CUST001",
                "transaction_date": "2026-08-01 10:00:00",
                "amount": 100.00,
                "currency": "USD",
                "country": "United States",
            },
            {
                "transaction_id": "TXN_TEST_002",
                "customer_id": "CUST002",
                "transaction_date": "2026-08-01 10:05:00",
                "amount": -50.00,
                "currency": "USD",
                "country": "United States",
            },
            {
                "transaction_id": "TXN_TEST_003",
                "customer_id": None,
                "transaction_date": "2026-08-01 10:10:00",
                "amount": 75.00,
                "currency": "USD",
                "country": "United States",
            },
            {
                "transaction_id": "TXN_TEST_004",
                "customer_id": "CUST004",
                "transaction_date": "2026-08-01 10:15:00",
                "amount": 200.00,
                "currency": "XYZ",
                "country": "United States",
            },
            {
                "transaction_id": "TXN_TEST_005",
                "customer_id": "CUST005",
                "transaction_date": "not-a-date",
                "amount": 300.00,
                "currency": "USD",
                "country": "United States",
            },
            {
                "transaction_id": "TXN_TEST_006",
                "customer_id": None,
                "transaction_date": "not-a-date",
                "amount": -100.00,
                "currency": "XYZ",
                "country": "United States",
            },
        ]
    )

    valid_df, rejected_df = validate_transactions(test_data)

    print("=== VALIDATION TEST RESULTS ===")
    print()
    print(f"Input records: {len(test_data)}")
    print(f"Valid records: {len(valid_df)}")
    print(f"Rejected records: {len(rejected_df)}")

    print()
    print("=== REJECTION REASONS ===")

    print(
        rejected_df[
            ["transaction_id", "rejection_reason"]
        ].to_string(index=False)
    )


if __name__ == "__main__":
    main()