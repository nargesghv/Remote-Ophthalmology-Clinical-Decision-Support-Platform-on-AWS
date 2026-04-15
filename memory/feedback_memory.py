from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from memory.memory_schema import FeedbackMemoryRecord


class FeedbackMemoryStore:
    def __init__(self, path: str = "data/feedback/feedback_memory.jsonl") -> None:
        self.path = Path(path)
        self.path.parent.mkdir(parents=True, exist_ok=True)

    def add(self, record: FeedbackMemoryRecord) -> None:
        with self.path.open("a", encoding="utf-8") as f:
            f.write(json.dumps(record.to_dict()) + "\n")

    def all(self) -> list[dict[str, Any]]:
        if not self.path.exists():
            return []
        return [json.loads(x) for x in self.path.read_text(encoding="utf-8").splitlines() if x.strip()]
