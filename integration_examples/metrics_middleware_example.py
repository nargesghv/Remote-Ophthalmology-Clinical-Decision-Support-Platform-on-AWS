from __future__ import annotations

import time

from monitoring.metrics.api_metrics import REQUEST_COUNT, REQUEST_LATENCY


async def metrics_middleware(request, call_next):
    start = time.time()
    status_code = 500
    endpoint = request.url.path
    method = request.method

    try:
        response = await call_next(request)
        status_code = response.status_code
        return response
    finally:
        duration = time.time() - start
        REQUEST_COUNT.labels(endpoint=endpoint, method=method, status=str(status_code)).inc()
        REQUEST_LATENCY.labels(endpoint=endpoint).observe(duration)
