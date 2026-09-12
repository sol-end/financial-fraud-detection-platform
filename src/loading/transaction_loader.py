import pandas as pd

from src.database.connection import get_connection


FACT_TRANSACTION_COLUMNS = [
    "transaction_id",
    "customer_id",
    "transaction_date",
    "amount",
    "currency",
    "merchant_id",
    "merchant_category",
    "payment_method",
    "country",
    "device_id",
    "ip_address",
    "fraud_score",
    "fraud_flag",
    "fraud_reason",
    "risk_decision",
]


def load_fact_transactions(df: pd.DataFrame):
    """
    Load scored transactions into fraud.fact_transactions.

    Existing transaction IDs are updated.
    New transaction IDs are inserted.
    """

    missing_columns = [
        column
        for column in FACT_TRANSACTION_COLUMNS
        if column not in df.columns
    ]

    if missing_columns:
        raise ValueError(
            f"Missing required columns: {missing_columns}"
        )

    connection = get_connection()

    try:
        with connection.cursor() as cursor:
            sql = """
                INSERT INTO fraud.fact_transactions (
                    transaction_id,
                    customer_id,
                    transaction_date,
                    amount,
                    currency,
                    merchant_id,
                    merchant_category,
                    payment_method,
                    country,
                    device_id,
                    ip_address,
                    fraud_score,
                    fraud_flag,
                    fraud_reason,
                    risk_decision
                )
                VALUES (
                    %s, %s, %s, %s, %s,
                    %s, %s, %s, %s, %s,
                    %s, %s, %s, %s, %s
                )
                ON CONFLICT (transaction_id)
                DO UPDATE SET
                    customer_id = EXCLUDED.customer_id,
                    transaction_date = EXCLUDED.transaction_date,
                    amount = EXCLUDED.amount,
                    currency = EXCLUDED.currency,
                    merchant_id = EXCLUDED.merchant_id,
                    merchant_category = EXCLUDED.merchant_category,
                    payment_method = EXCLUDED.payment_method,
                    country = EXCLUDED.country,
                    device_id = EXCLUDED.device_id,
                    ip_address = EXCLUDED.ip_address,
                    fraud_score = EXCLUDED.fraud_score,
                    fraud_flag = EXCLUDED.fraud_flag,
                    fraud_reason = EXCLUDED.fraud_reason,
                    risk_decision = EXCLUDED.risk_decision,
                    updated_at = CURRENT_TIMESTAMP;
            """

            for row in df[FACT_TRANSACTION_COLUMNS].itertuples(
                index=False,
                name=None,
            ):
                cursor.execute(sql, row)

        connection.commit()

        return len(df)

    except Exception:
        connection.rollback()
        raise

    finally:
        connection.close()


def load_rejected_transactions(df: pd.DataFrame):
    """
    Load validation-rejected transactions into
    fraud.rejected_transactions.
    """

    required_columns = [
        "transaction_id",
        "source_file",
        "rejection_reason",
    ]

    missing_columns = [
        column
        for column in required_columns
        if column not in df.columns
    ]

    if missing_columns:
        raise ValueError(
            f"Missing required columns: {missing_columns}"
        )

    connection = get_connection()

    try:
        with connection.cursor() as cursor:
             
            inserted_count = 0
            sql = """
                INSERT INTO fraud.rejected_transactions (
                    transaction_id,
                    source_file,
                    rejection_reason
                )
                VALUES (%s, %s, %s)
                ON CONFLICT (
                    transaction_id,
                    source_file,
                    rejection_reason
                 )
                 DO NOTHING;
            """

            for row in df[required_columns].itertuples(
                index=False,
                name=None,
            ):
                cursor.execute(sql, row)

                if cursor.rowcount == 1:
                    inserted_count += 1

        connection.commit()

        return inserted_count

    except Exception:
        connection.rollback()
        raise

    finally:
        connection.close()
