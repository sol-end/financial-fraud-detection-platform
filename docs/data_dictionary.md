# Data Dictionary

## `fraud.stg_transactions`

Temporary staging table for ingested transaction records.

| Column | Description |
|---|---|
| `transaction_sk` | Surrogate key |
| `transaction_id` | Business transaction identifier |
| `customer_id` | Customer identifier |
| `transaction_date` | Date and time of transaction |
| `amount` | Transaction amount |
| `currency` | Three-letter currency code |
| `merchant_id` | Merchant identifier |
| `merchant_category` | Merchant category |
| `payment_method` | Payment method |
| `country` | Transaction country |
| `device_id` | Device identifier |
| `ip_address` | IP address associated with transaction |
| `source_file` | Source input file |
| `loaded_at` | Timestamp when record was loaded |

## `fraud.fact_transactions`

Primary table containing validated and fraud-scored transactions.

| Column | Description |
|---|---|
| `transaction_sk` | Surrogate key |
| `transaction_id` | Unique transaction identifier |
| `customer_id` | Customer identifier |
| `transaction_date` | Date and time of transaction |
| `amount` | Transaction amount |
| `currency` | Currency code |
| `merchant_id` | Merchant identifier |
| `merchant_category` | Merchant category |
| `payment_method` | Payment method |
| `country` | Transaction country |
| `device_id` | Device identifier |
| `ip_address` | IP address |
| `fraud_score` | Calculated fraud risk score |
| `fraud_flag` | Indicates whether transaction is flagged |
| `fraud_reason` | Explanation for fraud classification |
| `risk_decision` | APPROVE, REVIEW, or DECLINE |
| `created_at` | Record creation timestamp |
| `updated_at` | Last update timestamp |

## `fraud.rejected_transactions`

Stores transactions that failed validation.

| Column | Description |
|---|---|
| `rejected_sk` | Surrogate key |
| `transaction_id` | Transaction identifier |
| `source_file` | Source input file |
| `rejection_reason` | Reason the transaction was rejected |
| `rejected_at` | Rejection timestamp |

The combination of `transaction_id`, `source_file`, and `rejection_reason` is unique to support idempotent loading.

## `fraud.pipeline_audit`

Tracks every pipeline execution.

| Column | Description |
|---|---|
| `pipeline_run_id` | Unique pipeline execution ID |
| `pipeline_name` | Pipeline name |
| `status` | RUNNING, SUCCESS, or FAILED |
| `start_time` | Pipeline start timestamp |
| `end_time` | Pipeline completion timestamp |
| `raw_count` | Number of raw transactions |
| `valid_count` | Number of valid transactions |
| `rejected_count` | Number of rejected transactions |
| `transformed_count` | Number of transformed transactions |
| `scored_count` | Number of scored transactions |
| `fraud_flagged_count` | Number of flagged transactions |
| `approve_count` | Number of APPROVE decisions |
| `review_count` | Number of REVIEW decisions |
| `decline_count` | Number of DECLINE decisions |
| `fact_loaded_count` | Number of fact records loaded |
| `rejected_loaded_count` | Number of rejected records loaded |
| `error_message` | Error details when a run fails |

## Validation Rules

Transactions can be rejected for conditions including:

- Missing required fields
- Invalid transaction amount
- Invalid currency
- Invalid transaction date
- Duplicate transaction ID

