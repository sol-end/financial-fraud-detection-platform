# Project Design

## Purpose

The Financial Fraud Detection Platform is an end-to-end data engineering project designed to ingest financial transactions, validate data quality, transform records, calculate fraud risk, and load the results into PostgreSQL.

## Design Goals

- Build a complete data pipeline from ingestion to database loading.
- Separate each pipeline responsibility into its own module.
- Reject invalid transactions without stopping the entire pipeline.
- Calculate a fraud score and risk decision for valid transactions.
- Maintain an audit record for every pipeline execution.
- Make database loading idempotent.
- Provide automated tests and CI validation.

## Pipeline Flow

1. **Ingestion** — Read transaction CSV files.
2. **Validation** — Identify valid and rejected transactions.
3. **Transformation** — Standardize and prepare valid transactions.
4. **Fraud Detection** — Calculate fraud scores and risk decisions.
5. **Loading** — Store valid transactions in the fact table and rejected records separately.
6. **Audit** — Record pipeline status, counts, and failures.

## Database Design

The PostgreSQL database uses the `fraud` schema.

Main tables:

- `fraud.stg_transactions` — staging transaction data.
- `fraud.fact_transactions` — validated and scored transactions.
- `fraud.rejected_transactions` — transactions rejected during validation.
- `fraud.pipeline_audit` — pipeline execution history.

## Reliability

The platform includes:

- Transaction validation
- Database transaction rollback
- Rejected-record tracking
- Idempotent loading
- Pipeline failure auditing
- Automated tests
- Continuous integration

## Testing

The project currently contains:

- 29 automated tests
- 100% code coverage
- PostgreSQL integration tests
- CI execution through GitHub Actions

