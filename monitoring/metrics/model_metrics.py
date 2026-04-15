from prometheus_client import Counter, Gauge, Histogram

QUALITY_REJECTION_RATE = Gauge(
    "quality_rejection_rate",
    "Rate of rejected images due to low quality"
)

DISEASE_CONFIDENCE = Gauge(
    "disease_prediction_confidence",
    "Latest disease prediction confidence",
    ["disease_label"],
)

MODEL_INFERENCE_ERRORS = Counter(
    "model_inference_errors_total",
    "Number of model inference failures",
    ["model_name"],
)

MODEL_INFERENCE_LATENCY = Histogram(
    "model_inference_latency_seconds",
    "Model inference latency in seconds",
    ["model_name"],
)
