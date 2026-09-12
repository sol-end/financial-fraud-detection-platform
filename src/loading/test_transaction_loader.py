import pandas as pd

from src.loading.transaction_loader import load_fact_transactions


def main():
    test_data = pd.DataFrame(
        [
            {
                "transaction_id": "TXN_LOADER_TEST_001",
                "customer_id": "CUST_TEST_001",
                "transaction_date": pd.Timestamp("2026-09-04 10:00:00"),
                "amount": 125.50,
                "currency": "USD",
                "merchant_id": "MERCH_TEST_001",
                "merchant_category": "Grocery",
                "payment_method": "Credit Card",
                "country": "United States",
                "device_id": "DEV_TEST_001",
                "ip_address": "192.168.1.100",
                "fraud_score": 0.0,
                "fraud_flag": False,
                "fraud_reason": None,
                "risk_decision": "APPROVE",
            }
        ]
    )

    loaded_count = load_fact_transactions(test_data)

    print("=== LOADER TEST ===")
    print(f"Records supplied: {len(test_data)}")
    print(f"Records loaded: {loaded_count}")
    print("✅ Loader test completed successfully.")


if __name__ == "__main__":
    main()
