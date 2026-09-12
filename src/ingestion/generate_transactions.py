from pathlib import Path

import numpy as np
import pandas as pd


PROJECT_ROOT = Path(__file__).resolve().parents[2]
INCOMING_DIR = PROJECT_ROOT / "data" / "incoming"

RANDOM_SEED = 42
TOTAL_TRANSACTIONS = 10_000
FILES_TO_CREATE = 3


def generate_transactions():
    """Generate synthetic financial transaction data."""

    rng = np.random.default_rng(RANDOM_SEED)

    customer_ids = [f"CUST{i:05d}" for i in range(1, 2001)]
    merchant_ids = [f"MERCH{i:05d}" for i in range(1, 501)]

    merchant_categories = [
        "Grocery",
        "Restaurant",
        "Retail",
        "Travel",
        "Electronics",
        "Entertainment",
        "Healthcare",
        "Gas",
        "Online Services",
        "Luxury Goods",
    ]

    payment_methods = [
        "Credit Card",
        "Debit Card",
        "Bank Transfer",
        "Mobile Wallet",
    ]

    countries = [
        "United States",
        "Canada",
        "United Kingdom",
        "Germany",
        "France",
        "Australia",
        "Japan",
        "Brazil",
        "Mexico",
        "Nigeria",
    ]

    transaction_dates = pd.date_range(
        start="2026-01-01",
        end="2026-08-31",
        periods=TOTAL_TRANSACTIONS,
    )

    data = {
        "transaction_id": [
            f"TXN{i:08d}" for i in range(1, TOTAL_TRANSACTIONS + 1)
        ],
        "customer_id": rng.choice(customer_ids, TOTAL_TRANSACTIONS),
        "transaction_date": transaction_dates,
        "amount": np.round(
            rng.lognormal(mean=4.2, sigma=1.1, size=TOTAL_TRANSACTIONS),
            2,
        ),
        "currency": rng.choice(
            ["USD", "CAD", "GBP", "EUR", "AUD"],
            TOTAL_TRANSACTIONS,
            p=[0.75, 0.07, 0.06, 0.07, 0.05],
        ),
        "merchant_id": rng.choice(merchant_ids, TOTAL_TRANSACTIONS),
        "merchant_category": rng.choice(
            merchant_categories,
            TOTAL_TRANSACTIONS,
        ),
        "payment_method": rng.choice(
            payment_methods,
            TOTAL_TRANSACTIONS,
        ),
        "country": rng.choice(
            countries,
            TOTAL_TRANSACTIONS,
            p=[0.65, 0.07, 0.05, 0.04, 0.04, 0.03, 0.03, 0.03, 0.02, 0.04],
        ),
        "device_id": [
            f"DEV{i:06d}" for i in rng.integers(1, 4001, TOTAL_TRANSACTIONS)
        ],
        "ip_address": [
            f"192.168.{rng.integers(0, 256)}.{rng.integers(1, 255)}"
            for _ in range(TOTAL_TRANSACTIONS)
        ],
    }

    df = pd.DataFrame(data)

    # Plant intentionally suspicious transactions.
    high_amount_indices = rng.choice(
        df.index,
        size=100,
        replace=False,
    )
    df.loc[high_amount_indices, "amount"] = np.round(
        rng.uniform(5_000, 25_000, len(high_amount_indices)),
        2,
    )

    suspicious_country_indices = rng.choice(
        df.index,
        size=100,
        replace=False,
    )
    df.loc[suspicious_country_indices, "country"] = "Nigeria"

    suspicious_category_indices = rng.choice(
        df.index,
        size=100,
        replace=False,
    )
    df.loc[
        suspicious_category_indices,
        "merchant_category",
    ] = "Luxury Goods"

    # Create repeated device activity.
    suspicious_device_indices = rng.choice(
        df.index,
        size=100,
        replace=False,
    )
    df.loc[
        suspicious_device_indices,
        "device_id",
    ] = "DEV_SUSPICIOUS"

    # Add invalid records for validation testing.
    invalid_amount_indices = rng.choice(
        df.index,
        size=20,
        replace=False,
    )
    df.loc[invalid_amount_indices, "amount"] = -10.00

    missing_customer_indices = rng.choice(
        df.index,
        size=20,
        replace=False,
    )
    df.loc[missing_customer_indices, "customer_id"] = None

    # Split the dataset across multiple incoming files.
        # Split the dataset across multiple incoming files.
    rows_per_file = len(df) // FILES_TO_CREATE

    INCOMING_DIR.mkdir(parents=True, exist_ok=True)

    for index in range(FILES_TO_CREATE):
        start_row = index * rows_per_file

        if index == FILES_TO_CREATE - 1:
            end_row = len(df)
        else:
            end_row = start_row + rows_per_file

        chunk = df.iloc[start_row:end_row]

        output_file = (
            INCOMING_DIR / f"transactions_part_{index + 1:02d}.csv"
        )

        chunk.to_csv(output_file, index=False)

        print(
            f"Created {output_file.name}: "
            f"{len(chunk):,} rows"
        )

if __name__ == "__main__":
    generate_transactions()
