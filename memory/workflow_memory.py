from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any


@dataclass
class WorkflowMemory:
    case_id: str
    state: dict[str, Any] = field(default_factory=dict)

    def set(self, key: str, value: Any) -> None:
        self.state[key] = value

    def get(self, key: str, default: Any = None) -> Any:
        return self.state.get(key, default)

    def snapshot(self) -> dict[str, Any]:
        return {"case_id": self.case_id, "state": self.state.copy()}
