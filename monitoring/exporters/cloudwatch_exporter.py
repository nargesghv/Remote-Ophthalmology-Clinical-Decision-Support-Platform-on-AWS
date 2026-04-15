def emit_cloudwatch_metric(metric_name: str, value: float, unit: str = "Count") -> dict:
    return {
        "metric_name": metric_name,
        "value": value,
        "unit": unit,
        "status": "stub_only",
    }
