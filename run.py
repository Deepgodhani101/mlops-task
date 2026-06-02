import argparse
import json
import logging
import os
import time
import numpy as np
import pandas as pd
import yaml

def setup_logging(log_file):
    logging.basicConfig(
        filename=log_file,
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s - %(message)s"
    )

def write_error(output_file, version, message):
    metrics = {
        "version": version,
        "status": "error",
        "error_message": message
    }
    with open(output_file, "w") as f:
        json.dump(metrics, f, indent=4)
    print(json.dumps(metrics, indent=4))

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", required=True)
    parser.add_argument("--config", required=True)
    parser.add_argument("--output", required=True)
    parser.add_argument("--log-file", required=True)

    args = parser.parse_args()

    setup_logging(args.log_file)

    start = time.time()
    version = "v1"

    try:
        logging.info("Job started")

        with open(args.config, "r") as f:
            config = yaml.safe_load(f)

        seed = config["seed"]
        window = config["window"]
        version = config["version"]

        np.random.seed(seed)

        logging.info(f"Config loaded: {config}")

        if not os.path.exists(args.input):
            raise FileNotFoundError("Input file not found")

        df = pd.read_csv(args.input)

        if df.empty:
            raise ValueError("CSV file is empty")

        if "close" not in df.columns:
            raise ValueError("Missing close column")

        logging.info(f"Rows loaded: {len(df)}")

        df["rolling_mean"] = df["close"].rolling(window=window).mean()

        df["signal"] = (
            (df["close"] > df["rolling_mean"])
            .fillna(False)
            .astype(int)
        )

        signal_rate = round(float(df["signal"].mean()), 4)

        latency_ms = int((time.time() - start) * 1000)

        metrics = {
            "version": version,
            "rows_processed": len(df),
            "metric": "signal_rate",
            "value": signal_rate,
            "latency_ms": latency_ms,
            "seed": seed,
            "status": "success"
        }

        with open(args.output, "w") as f:
            json.dump(metrics, f, indent=4)

        logging.info("Job completed successfully")

        print(json.dumps(metrics, indent=4))

    except Exception as e:
        logging.exception(str(e))
        write_error(args.output, version, str(e))
        raise

if __name__ == "__main__":
    main()
