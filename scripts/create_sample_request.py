from pathlib import Path
import json
import base64

payload = {
    "patient_id": "patient-demo-1",
    "clinic_id": "clinic-zurich-1",
    "age": 72,
    "symptom_score": 8,
    "image_b64": base64.b64encode(b"demo image payload that is long enough to pass quality").decode("utf-8"),
    "complaint": "Blurred vision and occasional eye pain",
}

out = Path("data/manifests/sample_request.json")
out.parent.mkdir(parents=True, exist_ok=True)
out.write_text(json.dumps(payload, indent=2), encoding="utf-8")
print(f"Wrote {out}")
