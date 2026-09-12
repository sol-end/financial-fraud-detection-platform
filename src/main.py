
import logging

from src.audit.pipeline_audit import (
    complete_pipeline_run,
    fail_pipeline_run,
    start_pipeline_run,
)
from src.utils.logging_config import configure_logging
from src.fraud_detection.fraud_detector import calculate_fraud_score
from src.ingestion.csv_reader import read_all_transaction_files
from src.loading.transaction_loader import (
    load_fact_transactions,
    load_rejected_transactions,
)
from src.transformation.transaction_transformer import transform_transactions
from src.validation.transaction_validator import validate_transactions


logger = logging.getLogger(__name__)


def run_pipeline():
    """Run the complete financial fraud detection pipeline."""

    configure_logging()

    pipeline_run_id = start_pipeline_run()

    logger.info(
        "Financial fraud detection pipeline started. "
        "Pipeline run ID: %s",
        pipeline_run_id,
    )

    print("=== FINANCIAL FRAUD DETECTION PIPELINE ===")
    print(f"Pipeline run ID: {pipeline_run_id}")
    print()

    try:
       # 1. Ingestion
        print("[1/5] Reading transaction files...")

        logger.info("Ingestion stage started.")

        raw_df = read_all_transaction_files()

        logger.info(
        "Ingestion stage completed. Raw transactions: %s",
        len(raw_df),
        )

        print(f"      Raw transactions: {len(raw_df):,}")
        print()

        # 2. Validation
        print("[2/5] Validating transactions...")

        logger.info("Validation stage started.")

        valid_df, rejected_df = validate_transactions(raw_df)

        logger.info(
        "Validation stage completed. "
        "Valid transactions: %s. Rejected transactions: %s.",
        len(valid_df),
        len(rejected_df),
        )

        print(f"      Valid transactions: {len(valid_df):,}")
        print(f"      Rejected transactions: {len(rejected_df):,}")
        print()

        # 3. Transformation
        
        print("[3/5] Transforming valid transactions...")

        logger.info("Transformation stage started.")

        transformed_df = transform_transactions(valid_df)

        logger.info(
        "Transformation stage completed. "
        "Transformed transactions: %s.",
        len(transformed_df),
        )

        print(f"      Transformed transactions: {len(transformed_df):,}")
        print()

     # 4. Fraud detection
        print("[4/5] Calculating fraud scores and decisions...")

        logger.info("Fraud detection stage started.")

        scored_df = calculate_fraud_score(transformed_df)

        fraud_flagged_count = int(
        scored_df["fraud_flag"].sum()
        )

        decision_counts = (
        scored_df["risk_decision"]
        .value_counts()
        .to_dict()
        )

        logger.info(
        "Fraud detection stage completed. "
        "Scored transactions: %s. Fraud flagged: %s.",
        len(scored_df),
        fraud_flagged_count,
        )

        logger.info(
        "Risk decisions — APPROVE: %s, REVIEW: %s, DECLINE: %s.",
        decision_counts.get("APPROVE", 0),
        decision_counts.get("REVIEW", 0),
        decision_counts.get("DECLINE", 0),
        )

        print(f"      Scored transactions: {len(scored_df):,}")
        print()

        
       # 5. Loading
        print("[5/5] Loading transactions into PostgreSQL...")

        logger.info(
        "Loading stage started. "
        "Scored transactions: %s. Rejected transactions: %s.",
        len(scored_df),
        len(rejected_df),
        )

        fact_loaded_count = load_fact_transactions(scored_df)

        rejected_loaded_count = load_rejected_transactions(
        rejected_df
        )

        logger.info(
        "Fact transactions loaded: %s.",
        fact_loaded_count,
        )

        logger.info(
        "Rejected transactions loaded: %s.",
        rejected_loaded_count,
        )

        logger.info(
        "Loading stage completed. "
        "Fact loaded: %s. Rejected loaded: %s.",
        fact_loaded_count,
        rejected_loaded_count,
        )

        print(
        f"      Fact transactions loaded: "
        f"{fact_loaded_count:,}"
        )

        print(
        f"      Rejected transactions loaded: "
        f"{rejected_loaded_count:,}"
        )

        print()

        # Mark the pipeline run as successful.
        complete_pipeline_run(
            pipeline_run_id=pipeline_run_id,
            raw_count=len(raw_df),
            valid_count=len(valid_df),
            rejected_count=len(rejected_df),
            transformed_count=len(transformed_df),
            scored_count=len(scored_df),
            fact_loaded_count=fact_loaded_count,
            rejected_loaded_count=rejected_loaded_count,
        )

        logger.info(
            "Financial fraud detection pipeline completed successfully. "
            "Pipeline run ID: %s",
            pipeline_run_id,
        )

        print("=== PIPELINE COMPLETE ===")

        return {
            "pipeline_run_id": pipeline_run_id,
            "raw_count": len(raw_df),
            "valid_count": len(valid_df),
            "rejected_count": len(rejected_df),
            "transformed_count": len(transformed_df),
            "scored_count": len(scored_df),
            "fact_loaded_count": fact_loaded_count,
            "rejected_loaded_count": rejected_loaded_count,
        }

    except Exception as error:
        error_message = f"{type(error).__name__}: {error}"

        logger.exception(
            "Financial fraud detection pipeline failed. "
            "Pipeline run ID: %s",
            pipeline_run_id,
        )

        fail_pipeline_run(
            pipeline_run_id=pipeline_run_id,
            error_message=error_message,
        )

        print()
        print("=== PIPELINE FAILED ===")
        print(f"Error: {error_message}")

        raise


if __name__ == "__main__":
    run_pipeline()

