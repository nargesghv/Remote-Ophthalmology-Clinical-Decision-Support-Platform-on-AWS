from __future__ import annotations

from app import db


def enqueue_case(case_id: str, priority: str) -> None:
    db.enqueue_case(case_id, priority)


def get_pending_cases() -> list[dict]:
    return db.get_pending_queue()
