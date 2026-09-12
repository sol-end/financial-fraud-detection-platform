import pandas as pd


TEXT_COLUMNS = [
    "transaction_id",
    "customer_id",
    "currency",
    "merchant_id",
    "merchant_category",
    "payment_method",
    "country",
    "device_id",
    "ip_address",
]


def transform_transactions(df: pd.DataFrame) -> pd.DataFrame:
    """
    Transform validated transaction records for downstream processing.

    Responsibilities:
    - Preserve the validated records.
    - Convert transaction_date to datetime.
    - Normalize text fields by removing surrounding whitespace.
    - Return a new DataFrame without modifying the input.
    """

    transformed_df = df.copy()

    # Normalize text fields.
    for column in TEXT_COLUMNS:
        transformed_df[column] = (
            transformed_df[column]
            .astype(str)
            .str.strip()
        )

    # Convert transaction date to a proper datetime type.
    transformed_df["transaction_date"] = pd.to_datetime(
        transformed_df["transaction_date"],
        errors="raise",
    )

    # Ensure amount is numeric.
    transformed_df["amount"] = pd.to_numeric(
        transformed_df["amount"],
        errors="raise",
    )

    return transformed_df