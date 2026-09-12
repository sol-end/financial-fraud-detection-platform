ALTER TABLE fraud.fact_transactions
ADD COLUMN IF NOT EXISTS risk_decision VARCHAR(20);
