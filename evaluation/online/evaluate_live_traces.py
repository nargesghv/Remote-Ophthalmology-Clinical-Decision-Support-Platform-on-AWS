from __future__ import annotations


def summarize_live_traces(traces: list[dict]) -> dict:
    total = len(traces)
    fallbacks = sum(1 for t in traces if t.get("used_fallback"))
    avg_latency = sum(t.get("latency", 0.0) for t in traces) / total if total else 0.0
    return {
        "num_traces": total,
        "fallback_rate": fallbacks / total if total else 0.0,
        "avg_latency": avg_latency,
    }
