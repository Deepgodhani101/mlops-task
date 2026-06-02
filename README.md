# ML/MLOps Technical Assessment

## Overview

This project implements a lightweight MLOps-style batch processing pipeline for financial market data. The application reads OHLCV data, calculates a rolling moving average on closing prices, generates binary trading signals, and produces structured metrics and logs for monitoring and observability.

The solution demonstrates:

* Reproducibility through YAML-based configuration and deterministic execution
* Data validation and error handling
* Observability through structured logging and machine-readable metrics
* Deployment readiness through Docker containerization

---

## Project Structure

```
.
├── run.py
├── config.yaml
├── data.csv
├── requirements.txt
├── Dockerfile
├── README.md
├── metrics.json
└── run.log
```

---

## Processing Workflow

1. Load and validate configuration from YAML
2. Read and validate input CSV data
3. Compute rolling mean on the `close` column
4. Generate binary signals:

   * `1` if close > rolling_mean
   * `0` otherwise
5. Calculate execution metrics
6. Write metrics to JSON
7. Record execution details in logs

---

## Local Execution

```bash
pip install -r requirements.txt

python run.py \
--input data.csv \
--config config.yaml \
--output metrics.json \
--log-file run.log
```

---

## Docker Execution

Build image:

```bash
docker build -t mlops-task .
```

Run container:

```bash
docker run --rm mlops-task
```

---

## Example Output

```json
{
  "version": "v1",
  "rows_processed": 10000,
  "metric": "signal_rate",
  "value": 0.4990,
  "latency_ms": 127,
  "seed": 42,
  "status": "success"
}
```

---

## Technologies Used

* Python
* Pandas
* NumPy
* PyYAML
* Docker
* Git
