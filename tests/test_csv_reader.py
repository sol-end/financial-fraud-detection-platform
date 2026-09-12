from pathlib import Path

import pandas as pd
import pytest

import src.ingestion.csv_reader as csv_reader


def test_get_transaction_files_returns_csv_files(monkeypatch, tmp_path):
    csv_file_1 = tmp_path / "transactions_01.csv"
    csv_file_2 = tmp_path / "transactions_02.csv"
    txt_file = tmp_path / "notes.txt"

    csv_file_1.write_text("transaction_id,amount\nTXN001,100\n")
    csv_file_2.write_text("transaction_id,amount\nTXN002,200\n")
    txt_file.write_text("not a csv transaction file")

    monkeypatch.setattr(
        csv_reader,
        "INCOMING_DIR",
        tmp_path,
    )

    result = csv_reader.get_transaction_files()

    assert result == sorted([csv_file_1, csv_file_2])


def test_read_transaction_file_adds_source_filename(tmp_path):
    csv_file = tmp_path / "transactions.csv"

    csv_file.write_text(
        "transaction_id,amount\n"
        "TXN001,100\n"
        "TXN002,200\n"
    )

    result = csv_reader.read_transaction_file(csv_file)

    assert isinstance(result, pd.DataFrame)
    assert len(result) == 2
    assert "source_file" in result.columns
    assert result["source_file"].tolist() == [
        "transactions.csv",
        "transactions.csv",
    ]


def test_read_all_transaction_files_combines_csv_files(monkeypatch, tmp_path):
    csv_file_1 = tmp_path / "transactions_01.csv"
    csv_file_2 = tmp_path / "transactions_02.csv"

    csv_file_1.write_text(
        "transaction_id,amount\n"
        "TXN001,100\n"
        "TXN002,200\n"
    )

    csv_file_2.write_text(
        "transaction_id,amount\n"
        "TXN003,300\n"
    )

    monkeypatch.setattr(
        csv_reader,
        "INCOMING_DIR",
        tmp_path,
    )

    result = csv_reader.read_all_transaction_files()

    assert len(result) == 3
    assert result["transaction_id"].tolist() == [
        "TXN001",
        "TXN002",
        "TXN003",
    ]

    assert result["source_file"].tolist() == [
        "transactions_01.csv",
        "transactions_01.csv",
        "transactions_02.csv",
    ]


def test_read_all_transaction_files_raises_when_no_files(
    monkeypatch,
    tmp_path,
):
    monkeypatch.setattr(
        csv_reader,
        "INCOMING_DIR",
        tmp_path,
    )

    with pytest.raises(
        FileNotFoundError,
        match="No CSV transaction files found",
    ):
        csv_reader.read_all_transaction_files()