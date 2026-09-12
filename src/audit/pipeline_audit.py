
from src.database.connection import get_connection


PIPELINE_NAME = "financial_fraud_detection"


def start_pipeline_run():
    """
    Create a new pipeline audit record with RUNNING status.

    Returns:
        int: The generated pipeline_run_id.
    """

    connection = get_connection()

    try:
        with connection.cursor() as cursor:
            sql = """
                INSERT INTO fraud.pipeline_audit (
                    pipeline_name,
                    status
                )
                VALUES (%s, %s)
                RETURNING pipeline_run_id;
            """

            cursor.execute(
                sql,
                (PIPELINE_NAME, "RUNNING"),
            )

            pipeline_run_id = cursor.fetchone()[0]

        connection.commit()

        return pipeline_run_id

    except Exception:
        connection.rollback()
        raise

    finally:
        connection.close()


def complete_pipeline_run(
    pipeline_run_id,
    raw_count,
    valid_count,
    rejected_count,
    transformed_count,
    scored_count,
    fact_loaded_count,
    rejected_loaded_count,
):
    """
    Mark a pipeline run as SUCCESS and store its processing metrics.
    """

    connection = get_connection()

    try:
        with connection.cursor() as cursor:
            sql = """
                UPDATE fraud.pipeline_audit
                SET
                    status = %s,
                    end_time = CURRENT_TIMESTAMP,
                    raw_count = %s,
                    valid_count = %s,
                    rejected_count = %s,
                    transformed_count = %s,
                    scored_count = %s,
                    fact_loaded_count = %s,
                    rejected_loaded_count = %s
                WHERE pipeline_run_id = %s;
            """

            cursor.execute(
                sql,
                (
                    "SUCCESS",
                    raw_count,
                    valid_count,
                    rejected_count,
                    transformed_count,
                    scored_count,
                    fact_loaded_count,
                    rejected_loaded_count,
                    pipeline_run_id,
                ),
            )

        connection.commit()

    except Exception:
        connection.rollback()
        raise

    finally:
        connection.close()


def fail_pipeline_run(
    pipeline_run_id,
    error_message,
):
    """
    Mark a pipeline run as FAILED and store the error message.
    """

    connection = get_connection()

    try:
        with connection.cursor() as cursor:
            sql = """
                UPDATE fraud.pipeline_audit
                SET
                    status = %s,
                    end_time = CURRENT_TIMESTAMP,
                    error_message = %s
                WHERE pipeline_run_id = %s;
            """

            cursor.execute(
                sql,
                (
                    "FAILED",
                    error_message,
                    pipeline_run_id,
                ),
            )

        connection.commit()

    except Exception:
        connection.rollback()
        raise

    finally:
        connection.close()