# Financial Fraud Detection Platform

[![CI](https://github.com/sol-end/financial-fraud-detection-platform/actions/workflows/ci.yml/badge.svg)](https://github.com/sol-end/financial-fraud-detection-platform/actions/workflows/ci.yml)

A Python-based financial fraud detection platform demonstrating an end-to-end data engineering pipeline.

## Pipeline

CSV ingestion → validation → transformation → fraud detection → PostgreSQL loading → audit

## Tech Stack

- Python 3.14
- Pandas
- NumPy
- scikit-learn
- PostgreSQL
- psycopg2
- pytest
- GitHub Actions

## Testing

- 29 tests passing
- 100% code coverage
- 249 production statements covered
- PostgreSQL integration tests included

Run tests:

    pytest --cov=src --cov-report=term-missing

Run the pipeline:

    python -m src.main

## CI

GitHub Actions automatically runs the test suite on pushes and pull requests to main.

## Goals

This project demonstrates data ingestion, validation, transformation, fraud scoring, PostgreSQL loading, rejected-record handling, pipeline auditing, automated testing, CI/CD, and database idempotency.
