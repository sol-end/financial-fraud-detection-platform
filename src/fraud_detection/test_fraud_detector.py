import pandas as pd

from src.fraud_detection.fraud_detector import (
    calculate_fraud_score,
)


def main():
    test_data = pd.DataFrame(
        [
            {
                "transaction_id": "TXN_FRAUD_TEST_001",
                "customer_id": "CUST001",
                "transaction_date": "2026-08-01 10:00:00",
                "amount": 100.00,
                "currency": "USD",
                "merchant_id": "MERCH001",
                "merchant_category": "Grocery",
                "payment_method": "Credit Card",
                "country": "United States",
                "device_id": "DEV001",
                "ip_address": "192.168.1.10",
            },
            {
                "transaction_id": "TXN_FRAUD_TEST_002",
                "customer_id": "CUST002",
                "transaction_date": "2026-08-01 10:05:00",
                "amount": 7500.00,
                "currency": "USD",
                "merchant_id": "MERCH002",
                "merchant_category": "Retail",
                "payment_method": "Credit Card",
                "country": "United States",
                "device_id": "DEV002",
                "ip_address": "192.168.1.11",
            },
            {
                "transaction_id": "TXN_FRAUD_TEST_003",
                "customer_id": "CUST003",
                "transaction_date": "2026-08-01 10:10:00",
                "amount": 10000.00,
                "currency": "USD",
                "merchant_id": "MERCH003",
                "merchant_category": "Luxury Goods",
                "payment_method": "Credit Card",
                "country": "Nigeria",
                "device_id": "DEV_SUSPICIOUS",
                "ip_address": "192.168.1.12",
            },
            {
                "transaction_id": "TXN_FRAUD_TEST_004",
                "customer_id": "CUST004",
                "transaction_date": "2026-08-01 10:15:00",
                "amount": 100.00,
                "currency": "USD",
                "merchant_id": "MERCH004",
                "merchant_category": "Grocery",
                "payment_method": "Mobile Wallet",
                "country": "United States",
                "device_id": "DEV_SUSPICIOUS",
                "ip_address": "192.168.1.13",
            },
        ]
    )

    result_df = calculate_fraud_score(test_data)

    print("=== FRAUD DETECTION TEST RESULTS ===")
    print()

    print(
        result_df[
            [
                "transaction_id",
                "fraud_score",
                "fraud_flag",
                "fraud_reason",
                "risk_decision",
            ]
        ].to_string(index=False)
    )


if __name__ == "__main__":
    main()