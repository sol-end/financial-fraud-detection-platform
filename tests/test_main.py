import pandas as pd

import src.main as main


def test_run_pipeline_orchestrates_all_stages(monkeypatch):
    raw_df = pd.DataFrame(
        [
            {
                "transaction_id": "TXN_ORCH_001",
                "amount": 100.00,
            },
            {
                "transaction_id": "TXN_ORCH_002",
                "amount": 200.00,
            },
        ]
    )

    valid_df = raw_df.iloc[[0]].copy()

    rejected_df = pd.DataFrame(
        [
            {
                "transaction_id": "TXN_ORCH_002",
                "source_file": "test.csv",
                "rejection_reason": "Invalid amount",
            }
        ]
    )

    transformed_df = valid_df.copy()

    scored_df = transformed_df.copy()
    scored_df["fraud_score"] = 0.0
    scored_df["fraud_flag"] = False
    scored_df["risk_decision"] = "APPROVE"

    monkeypatch.setattr(
        main,
        "configure_logging",
        lambda: None,
    )

    monkeypatch.setattr(
        main,
        "start_pipeline_run",
        lambda: 123,
    )

    monkeypatch.setattr(
        main,
        "read_all_transaction_files",
        lambda: raw_df,
    )

    monkeypatch.setattr(
        main,
        "validate_transactions",
        lambda df: (valid_df, rejected_df),
    )

    monkeypatch.setattr(
        main,
        "transform_transactions",
        lambda df: transformed_df,
    )

    monkeypatch.setattr(
        main,
        "calculate_fraud_score",
        lambda df: scored_df,
    )

    monkeypatch.setattr(
        main,
        "load_fact_transactions",
        lambda df: 1,
    )

    monkeypatch.setattr(
        main,
        "load_rejected_transactions",
        lambda df: 1,
    )

    monkeypatch.setattr(
        main,
        "complete_pipeline_run",
        lambda **kwargs: None,
    )

    monkeypatch.setattr(
        main,
        "fail_pipeline_run",
        lambda **kwargs: None,
    )

    result = main.run_pipeline()

    assert result["pipeline_run_id"] == 123
    assert result["raw_count"] == 2
    assert result["valid_count"] == 1
    assert result["rejected_count"] == 1
    assert result["transformed_count"] == 1
    assert result["scored_count"] == 1
    assert result["fact_loaded_count"] == 1
    assert result["rejected_loaded_count"] == 1
def test_run_pipeline_records_failure_when_stage_fails(monkeypatch):
    failure_calls = []

    monkeypatch.setattr(
        main,
        "configure_logging",
        lambda: None,
    )

    monkeypatch.setattr(
        main,
        "start_pipeline_run",
        lambda: 456,
    )

    def failing_ingestion():
        raise RuntimeError("Simulated ingestion failure")

    monkeypatch.setattr(
        main,
        "read_all_transaction_files",
        failing_ingestion,
    )

    monkeypatch.setattr(
        main,
        "fail_pipeline_run",
        lambda **kwargs: failure_calls.append(kwargs),
    )

    try:
        main.run_pipeline()
        assert False, "Expected RuntimeError was not raised"
    except RuntimeError as error:
        assert str(error) == "Simulated ingestion failure"

    assert len(failure_calls) == 1

    assert failure_calls[0]["pipeline_run_id"] == 456
    assert (
        failure_calls[0]["error_message"]
        == "RuntimeError: Simulated ingestion failure"
    )
