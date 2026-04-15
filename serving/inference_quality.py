from __future__ import annotations

import base64
from pathlib import Path

from models.quality.inference_quality import predict_quality
from serving.capture_inference import capture_inference


def local_quality_endpoint(payload: dict) -> dict:
    image_b64 = payload["image_b64"]
    image_bytes = base64.b64decode(image_b64.encode("utf-8"))
    tmp_path = Path("artifacts/tmp_quality_image.bin")
    tmp_path.parent.mkdir(parents=True, exist_ok=True)
    tmp_path.write_bytes(image_bytes)

    # Reuse byte file as pseudo image path only for demo; in a real setup use actual image content.
    # The synthetic local training pipeline expects real image files, so this endpoint is mainly a stub.
    result = {
        "label": "good" if len(image_bytes) > 20 else "bad",
        "confidence": 0.92 if len(image_bytes) > 20 else 0.51,
        "model_version": "quality_endpoint_step2_v1",
    }
    capture_inference("quality_inference", {"payload_meta": {k: payload.get(k) for k in ("patient_id", "clinic_id")}, "result": result})
    return result
