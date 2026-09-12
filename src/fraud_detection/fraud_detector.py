import pandas as pd


HIGH_AMOUNT_THRESHOLD = 5000

RISK_SCORES = {
    "HIGH_AMOUNT": 40,
    "HIGH_RISK_COUNTRY": 20,
    "LUXURY_GOODS": 15,
    "SUSPICIOUS_DEVICE": 25,
}

HIGH_RISK_COUNTRIES = {"Nigeria"}


def calculate_fraud_score(df: pd.DataFrame) -> pd.DataFrame:
    """
    Calculate an explainable fraud risk score for each transaction.

    Every transaction is evaluated against every fraud rule.
    All triggered risk signals are preserved in fraud_reason.
    """

    result_df = df.copy()

    result_df["fraud_score"] = 0.0

    fraud_reasons = pd.Series(
        [[] for _ in range(len(result_df))],
        index=result_df.index,
        dtype=object,
    )

    # 1. High transaction amount
    high_amount = result_df["amount"] > HIGH_AMOUNT_THRESHOLD

    result_df.loc[high_amount, "fraud_score"] += (
        RISK_SCORES["HIGH_AMOUNT"]
    )

    for index in result_df.index[high_amount]:
        fraud_reasons.at[index].append("HIGH_AMOUNT")

    # 2. High-risk country
    high_risk_country = result_df["country"].isin(
        HIGH_RISK_COUNTRIES
    )

    result_df.loc[high_risk_country, "fraud_score"] += (
        RISK_SCORES["HIGH_RISK_COUNTRY"]
    )

    for index in result_df.index[high_risk_country]:
        fraud_reasons.at[index].append("HIGH_RISK_COUNTRY")

    # 3. Luxury goods
    luxury_goods = (
        result_df["merchant_category"] == "Luxury Goods"
    )

    result_df.loc[luxury_goods, "fraud_score"] += (
        RISK_SCORES["LUXURY_GOODS"]
    )

    for index in result_df.index[luxury_goods]:
        fraud_reasons.at[index].append("LUXURY_GOODS")

    # 4. Suspicious device
    suspicious_device = (
        result_df["device_id"] == "DEV_SUSPICIOUS"
    )

    result_df.loc[suspicious_device, "fraud_score"] += (
        RISK_SCORES["SUSPICIOUS_DEVICE"]
    )

    for index in result_df.index[suspicious_device]:
        fraud_reasons.at[index].append("SUSPICIOUS_DEVICE")

    # Store all triggered fraud signals.
    result_df["fraud_reason"] = fraud_reasons.apply(
        lambda reasons: ";".join(reasons) if reasons else None
    )

      # Flag transactions reaching the fraud threshold.
    result_df["fraud_flag"] = (
        result_df["fraud_score"] >= 50
    )

    # Assign an operational decision based on risk level.
    result_df["risk_decision"] = pd.cut(
        result_df["fraud_score"],
        bins=[-float("inf"), 34.99, 49.99, float("inf")],
        labels=["APPROVE", "REVIEW", "DECLINE"],
    )

    return result_df