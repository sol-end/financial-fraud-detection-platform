CREATE TABLE IF NOT EXISTS fraud.pipeline_audit (
    pipeline_run_id BIGSERIAL PRIMARY KEY,

    pipeline_name VARCHAR(100) NOT NULL,

    status VARCHAR(20) NOT NULL,

    start_time TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,

    end_time TIMESTAMP,

    raw_count INTEGER,

    valid_count INTEGER,

    rejected_count INTEGER,

    transformed_count INTEGER,

    scored_count INTEGER,

    fact_loaded_count INTEGER,

    rejected_loaded_count INTEGER,

    error_message TEXT,

    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);