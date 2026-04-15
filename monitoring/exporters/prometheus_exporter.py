from prometheus_client import generate_latest, CONTENT_TYPE_LATEST


def export_prometheus_metrics():
    return generate_latest().decode("utf-8"), CONTENT_TYPE_LATEST
