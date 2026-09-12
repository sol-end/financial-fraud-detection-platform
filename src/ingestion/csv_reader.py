from pathlib import Path

import pandas as pd


PROJECT_ROOT = Path(__file__).resolve().parents[2]
INCOMING_DIR = PROJECT_ROOT / "data" / "incoming"


def get_transaction_files():
    """Return all CSV transaction files from the incoming directory."""
    return sorted(INCOMING_DIR.glob("*.csv"))


def read_transaction_file(file_path):
    """Read a transaction CSV file and preserve its source filename."""

    df = pd.read_csv(file_path)

    df["source_file"] = file_path.name

    return df


def read_all_transaction_files():
    """Read and combine all incoming transaction CSV files."""

    files = get_transaction_files()

    if not files:
        raise FileNotFoundError(
            f"No CSV transaction files found in {INCOMING_DIR}"
        )

    dataframes = [
        read_transaction_file(file_path)
        for file_path in files
    ]

    return pd.concat(dataframes, ignore_index=True)
