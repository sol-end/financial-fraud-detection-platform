CREATE UNIQUE INDEX IF NOT EXISTS
    ux_rejected_transactions_audit
ON fraud.rejected_transactions (
    transaction_id,
    source_file,
    rejection_reason
);
