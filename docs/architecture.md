# System Architecture

## High-Level Flow

```text
                    ┌─────────────────┐
                    │   CSV Files     │
                    │ data/incoming/   │
                    └────────┬────────┘
                             │
                             ▼
                    ┌─────────────────┐
                    │    Ingestion    │
                    │   csv_reader    │
                    └────────┬────────┘
                             │
                             ▼
                    ┌─────────────────┐
                    │   Validation    │
                    │ transaction_    │
                    │    validator    │
                    └──────┬─────┬────┘
                           │     │
                    Valid  │     │ Rejected
                           ▼     ▼
                ┌─────────────┐  ┌──────────────────┐
                │Transformation│  │ Rejected Records │
                └──────┬──────┘  └────────┬─────────┘
                       │                  │
                       ▼                  ▼
                ┌─────────────┐   ┌──────────────────┐
                │Fraud Detection│  │ rejected_        │
                │ fraud_detector│  │ transactions     │
                └──────┬──────┘   └──────────────────┘
                       │
                       ▼
                ┌─────────────────┐
                │ Fact Transaction │
                │      Loader     │
                └────────┬────────┘
                         │
                         ▼
                ┌─────────────────┐
                │ fact_transactions│
                └─────────────────┘

                         │
                         ▼
                ┌─────────────────┐
                │ Pipeline Audit  │
                └─────────────────┘

