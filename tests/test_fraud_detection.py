import pandas as pd

from src.fraud_detection.fraud_detector import calculate_fraud_score


def test_normal_transaction_is_approved():
    df = pd.DataFrame(
        [
            {
                "transaction_id": "TEST_NORMAL",
                "customer_id": "CUST001",
                "transaction_date": "2026-08-01",
                "amount": 100.00,
                "currency": "USD",
                "merchant_id": "MERCH001",
                "merchant_category": "Grocery",
                "payment_method": "Credit Card",
                "country": "United States",
                "device_id": "DEV001",
                "ip_address": "192.168.1.1",
            }
        ]
    )

    result = calculate_fraud_score(df)

    assert result.iloc[0]["fraud_score"] == 0
    assert not result.iloc[0]["fraud_flag"]
    assert result.iloc[0]["risk_decision"] == "APPROVE"


def test_high_amount_transaction_is_declined_when_score_reaches_50():
    df = pd.DataFrame(
        [
            {
                "transaction_id": "TEST_HIGH_RISK",
                "customer_id": "CUST002",
                "transaction_date": "2026-08-01",
                "amount": 6000.00,
                "currency": "USD",
                "merchant_id": "MERCH002",
                "merchant_category": "Luxury Goods",
                "payment_method": "Credit Card",
                "country": "Nigeria",
                "device_id": "DEV_SUSPICIOUS",
                "ip_address": "192.168.1.2",
            }
        ]
    )

    result = calculate_fraud_score(df)

    assert result.iloc[0]["fraud_score"] == 100
    assert result.iloc[0]["fraud_flag"]
    assert result.iloc[0]["risk_decision"] == "DECLINE"
