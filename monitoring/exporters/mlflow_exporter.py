def log_mlflow_metric(run_id: str, key: str, value: float) -> dict:
    return {
        "run_id": run_id,
        "key": key,
        "value": value,
        "status": "stub_only",
    }
