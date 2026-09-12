import pandas as pd


VALID_CURRENCIES = {"USD", "EUR", "GBP", "CAD", "AUD"}

REQUIRED_COLUMNS = [
    "transaction_id",
    "customer_id",
    "transaction_date",
    "amount",
    "currency",
    "country",
]


def validate_transactions(df: pd.DataFrame):
    """
    Validate transaction records against all validation rules.

    Every record is evaluated against every validation rule.
    All applicable rejection reasons are collected.

    Returns:
        valid_df: DataFrame containing records with no validation failures.
        rejected_df: DataFrame containing invalid records and all
                     applicable rejection reasons.
    """

    df = df.copy()

    # Store all rejection reasons for each record.
    rejection_reasons = pd.Series(
        [[] for _ in range(len(df))],
        index=df.index,
        dtype=object,
    )

    # 1. Check required fields
    for column in REQUIRED_COLUMNS:
        missing_mask = df[column].isna() | (
            df[column].astype(str).str.strip() == ""
        )

        reason = f"MISSING_{column.upper()}"

        for index in df.index[missing_mask]:
            rejection_reasons.at[index].append(reason)

    # 2. Validate transaction amount
    numeric_amount = pd.to_numeric(
        df["amount"],
        errors="coerce",
    )

    invalid_amount = numeric_amount.isna() | (numeric_amount <= 0)

    for index in df.index[invalid_amount]:
        rejection_reasons.at[index].append("INVALID_AMOUNT")

    # 3. Validate currency
    invalid_currency = ~df["currency"].isin(VALID_CURRENCIES)

    for index in df.index[invalid_currency]:
        rejection_reasons.at[index].append("INVALID_CURRENCY")

    # 4. Validate transaction date
    parsed_dates = pd.to_datetime(
        df["transaction_date"],
        errors="coerce",
    )

    invalid_date = parsed_dates.isna()

    for index in df.index[invalid_date]:
        rejection_reasons.at[index].append(
            "INVALID_TRANSACTION_DATE"
        )

    # 5. Check duplicate transaction IDs
    duplicate_ids = df.duplicated(
        subset=["transaction_id"],
        keep="first",
    )

    for index in df.index[duplicate_ids]:
        rejection_reasons.at[index].append(
            "DUPLICATE_TRANSACTION_ID"
        )

    # Convert lists of reasons into a single readable string.
    df["rejection_reason"] = rejection_reasons.apply(
        lambda reasons: ";".join(reasons) if reasons else None
    )

    # Separate valid and rejected transactions.
    valid_df = df[
        df["rejection_reason"].isna()
    ].drop(columns=["rejection_reason"])

    rejected_df = df[
        df["rejection_reason"].notna()
    ]

    return valid_df, rejected_df