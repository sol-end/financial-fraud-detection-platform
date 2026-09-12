from src.ingestion.csv_reader import (
    get_transaction_files,
    read_all_transaction_files,
)


def main():
    files = get_transaction_files()

    print("Transaction files found:")
    for file_path in files:
        print(f"  - {file_path.name}")

    print()

    df = read_all_transaction_files()

    print(f"Total rows: {len(df):,}")
    print(f"Total columns: {len(df.columns)}")

    print("\nColumns:")
    for column in df.columns:
        print(f"  - {column}")

    print("\nFirst 5 rows:")
    print(df.head())


if __name__ == "__main__":
    main()
