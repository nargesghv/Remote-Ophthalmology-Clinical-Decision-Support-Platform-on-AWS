from __future__ import annotations

import json
import sqlite3
from contextlib import contextmanager
from datetime import datetime, timezone
from typing import Any

from app.config import settings


def _utc_now() -> str:
    return datetime.now(tz=timezone.utc).isoformat()


@contextmanager
def get_conn():
    conn = sqlite3.connect(settings.db_path, check_same_thread=False)
    conn.row_factory = sqlite3.Row
    try:
        yield conn
        conn.commit()
    finally:
        conn.close()


def init_db() -> None:
    with get_conn() as conn:
        conn.executescript(
            """
            CREATE TABLE IF NOT EXISTS cases (
                case_id TEXT PRIMARY KEY,
                patient_id TEXT NOT NULL,
                clinic_id TEXT NOT NULL,
                payload_json TEXT NOT NULL,
                status TEXT NOT NULL,
                created_at TEXT NOT NULL
            );

            CREATE TABLE IF NOT EXISTS workflow_runs (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                case_id TEXT NOT NULL,
                stage TEXT NOT NULL,
                state_json TEXT NOT NULL,
                created_at TEXT NOT NULL
            );

            CREATE TABLE IF NOT EXISTS predictions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                case_id TEXT NOT NULL,
                prediction_type TEXT NOT NULL,
                result_json TEXT NOT NULL,
                created_at TEXT NOT NULL
            );

            CREATE TABLE IF NOT EXISTS clinician_feedback (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                case_id TEXT NOT NULL,
                doctor_id TEXT NOT NULL,
                feedback_json TEXT NOT NULL,
                created_at TEXT NOT NULL
            );

            CREATE TABLE IF NOT EXISTS review_queue (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                case_id TEXT NOT NULL,
                priority TEXT NOT NULL,
                status TEXT NOT NULL,
                created_at TEXT NOT NULL
            );

            CREATE TABLE IF NOT EXISTS patient_background (
                patient_id TEXT PRIMARY KEY,
                background_json TEXT NOT NULL,
                updated_at TEXT NOT NULL
            );

            CREATE TABLE IF NOT EXISTS audit_events (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                case_id TEXT,
                event_type TEXT NOT NULL,
                payload_json TEXT NOT NULL,
                created_at TEXT NOT NULL
            );
            """
        )


def save_case(case_id: str, payload: dict[str, Any], status: str = "received") -> None:
    with get_conn() as conn:
        conn.execute(
            """
            INSERT INTO cases (case_id, patient_id, clinic_id, payload_json, status, created_at)
            VALUES (?, ?, ?, ?, ?, ?)
            """,
            (
                case_id,
                payload["patient_id"],
                payload["clinic_id"],
                json.dumps(payload),
                status,
                _utc_now(),
            ),
        )


def update_case_status(case_id: str, status: str) -> None:
    with get_conn() as conn:
        conn.execute("UPDATE cases SET status = ? WHERE case_id = ?", (status, case_id))


def get_case(case_id: str) -> dict[str, Any] | None:
    with get_conn() as conn:
        row = conn.execute("SELECT * FROM cases WHERE case_id = ?", (case_id,)).fetchone()
        if row is None:
            return None
        data = dict(row)
        data["payload_json"] = json.loads(data["payload_json"])
        return data


def save_prediction(case_id: str, prediction_type: str, result: dict[str, Any]) -> None:
    with get_conn() as conn:
        conn.execute(
            """
            INSERT INTO predictions (case_id, prediction_type, result_json, created_at)
            VALUES (?, ?, ?, ?)
            """,
            (case_id, prediction_type, json.dumps(result), _utc_now()),
        )


def save_workflow_state(case_id: str, stage: str, state: dict[str, Any]) -> None:
    with get_conn() as conn:
        conn.execute(
            """
            INSERT INTO workflow_runs (case_id, stage, state_json, created_at)
            VALUES (?, ?, ?, ?)
            """,
            (case_id, stage, json.dumps(state), _utc_now()),
        )


def save_clinician_feedback(case_id: str, doctor_id: str, feedback: dict[str, Any]) -> None:
    with get_conn() as conn:
        conn.execute(
            """
            INSERT INTO clinician_feedback (case_id, doctor_id, feedback_json, created_at)
            VALUES (?, ?, ?, ?)
            """,
            (case_id, doctor_id, json.dumps(feedback), _utc_now()),
        )


def enqueue_case(case_id: str, priority: str) -> None:
    with get_conn() as conn:
        conn.execute(
            """
            INSERT INTO review_queue (case_id, priority, status, created_at)
            VALUES (?, ?, 'pending', ?)
            """,
            (case_id, priority, _utc_now()),
        )


def get_pending_queue() -> list[dict[str, Any]]:
    with get_conn() as conn:
        rows = conn.execute(
            "SELECT * FROM review_queue WHERE status = 'pending' ORDER BY id ASC"
        ).fetchall()
        return [dict(row) for row in rows]


def seed_patient_background(patient_id: str, background: dict[str, Any]) -> None:
    with get_conn() as conn:
        conn.execute(
            """
            INSERT INTO patient_background (patient_id, background_json, updated_at)
            VALUES (?, ?, ?)
            ON CONFLICT(patient_id) DO UPDATE SET
                background_json=excluded.background_json,
                updated_at=excluded.updated_at
            """,
            (patient_id, json.dumps(background), _utc_now()),
        )


def get_patient_background(patient_id: str) -> dict[str, Any] | None:
    with get_conn() as conn:
        row = conn.execute(
            "SELECT background_json FROM patient_background WHERE patient_id = ?",
            (patient_id,),
        ).fetchone()
        if row is None:
            return None
        return json.loads(row["background_json"])


def audit_event(case_id: str | None, event_type: str, payload: dict[str, Any]) -> None:
    with get_conn() as conn:
        conn.execute(
            """
            INSERT INTO audit_events (case_id, event_type, payload_json, created_at)
            VALUES (?, ?, ?, ?)
            """,
            (case_id, event_type, json.dumps(payload), _utc_now()),
        )
