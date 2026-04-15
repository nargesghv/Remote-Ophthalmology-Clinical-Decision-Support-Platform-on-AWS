from __future__ import annotations

from serving.capture_inference import capture_inference


def local_summary_endpoint(payload: dict) -> dict:
    result = {
        "summary": (
            f"Summary: disease={payload['disease_result']['disease_name']}, "
            f"urgency={payload['reasoning_result']['urgency']}, "
            f"doctor review required."
        ),
        "summary_version": "summary_step2_v1",
    }
    capture_inference("summary_generation", {"result": result})
    return result
