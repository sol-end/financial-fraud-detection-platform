CREATE SCHEMA IF NOT EXISTS fraud;

CREATE TABLE IF NOT EXISTS fraud.stg_transactions (
    transaction_sk BIGSERIAL PRIMARY KEY,
    transaction_id VARCHAR(50) NOT NULL,
    customer_id VARCHAR(50) NOT NULL,
    transaction_date TIMESTAMP NOT NULL,
    amount NUMERIC(18,2) NOT NULL,
    currency VARCHAR(3) NOT NULL,
    merchant_id VARCHAR(50),
    merchant_category VARCHAR(100),
    payment_method VARCHAR(50),
    country VARCHAR(100),
    device_id VARCHAR(100),
    ip_address VARCHAR(45),
    source_file VARCHAR(255) NOT NULL,
    loaded_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS fraud.rejected_transactions (
    rejected_sk BIGSERIAL PRIMARY KEY,
    transaction_id VARCHAR(50),
    source_file VARCHAR(255),
    rejection_reason VARCHAR(255) NOT NULL,
    rejected_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS fraud.fact_transactions (
    transaction_sk BIGSERIAL PRIMARY KEY,
    transaction_id VARCHAR(50) NOT NULL UNIQUE,
    customer_id VARCHAR(50) NOT NULL,
    transaction_date TIMESTAMP NOT NULL,
    amount NUMERIC(18,2) NOT NULL,
    currency VARCHAR(3) NOT NULL,
    merchant_id VARCHAR(50),
    merchant_category VARCHAR(100),
    payment_method VARCHAR(50),
    country VARCHAR(100),
    device_id VARCHAR(100),
    ip_address VARCHAR(45),
    fraud_score NUMERIC(5,2),
    fraud_flag BOOLEAN DEFAULT FALSE,
    fraud_reason VARCHAR(255),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
