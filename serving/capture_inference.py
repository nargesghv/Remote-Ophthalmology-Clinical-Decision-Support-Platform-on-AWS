from __future__ import annotations

import json
from pathlib import Path
from datetime import datetime, timezone

LOG_PATH = Path("artifacts/inference_logs.jsonl")
LOG_PATH.parent.mkdir(parents=True, exist_ok=True)


def capture_inference(event_type: str, payload: dict) -> None:
    record = {
        "timestamp": datetime.now(tz=timezone.utc).isoformat(),
        "event_type": event_type,
        "payload": payload,
    }
    with LOG_PATH.open("a", encoding="utf-8") as f:
        f.write(json.dumps(record) + "\n")
