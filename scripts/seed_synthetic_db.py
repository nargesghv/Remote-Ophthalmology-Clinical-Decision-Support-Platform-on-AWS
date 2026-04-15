import sqlite3
import json
from pathlib import Path

db_path = Path("cases.db")
conn = sqlite3.connect(db_path)
conn.execute(
    '''
    CREATE TABLE IF NOT EXISTS patient_background (
        patient_id TEXT PRIMARY KEY,
        background_json TEXT NOT NULL,
        updated_at TEXT NOT NULL
    )
    '''
)

rows = [
    (
        "patient-demo-1",
        json.dumps({
            "conditions": ["diabetes"],
            "medications": ["metformin"],
            "allergies": ["penicillin"],
            "previous_diagnoses": ["mild retinopathy"]
        }),
        "2026-01-01T00:00:00Z",
    ),
    (
        "patient-demo-2",
        json.dumps({
            "conditions": ["hypertension"],
            "medications": ["amlodipine"],
            "allergies": [],
            "previous_diagnoses": []
        }),
        "2026-01-01T00:00:00Z",
    ),
]

conn.executemany(
    '''
    INSERT OR REPLACE INTO patient_background (patient_id, background_json, updated_at)
    VALUES (?, ?, ?)
    ''',
    rows,
)
conn.commit()
conn.close()
print(f"Seeded {db_path}")
