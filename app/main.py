from __future__ import annotations

import time
import uuid

from fastapi import Depends, FastAPI, HTTPException

from app import db
from app.auth import verify_api_key
from app.clinician_feedback import record_feedback
from app.config import settings
from app.model_clients import get_disease_client, get_quality_client
from app.orchestrator import WorkflowOrchestrator
from app.retrieval_clients import PatientBackgroundRetriever
from app.schemas import CaseResponse, FeedbackRequest, HealthResponse, IntakeRequest
from app.review_queue import get_pending_cases

app = FastAPI(title=settings.app_name, version="0.1.0")
STARTED_AT = time.time()

orchestrator = WorkflowOrchestrator(
    quality_client=get_quality_client(),
    disease_client=get_disease_client(),
    retrieval_client=PatientBackgroundRetriever(),
    use_llm_summary=settings.use_llm_summary,
)


@app.on_event("startup")
def startup() -> None:
    db.init_db()
    db.seed_patient_background(
        "patient-demo-1",
        {
            "conditions": ["diabetes"],
            "medications": ["metformin"],
            "allergies": ["penicillin"],
            "previous_diagnoses": ["mild retinopathy"],
        },
    )


@app.get("/health", response_model=HealthResponse)
def health() -> HealthResponse:
    return HealthResponse(
        status="ok",
        service=settings.app_name,
        uptime_seconds=round(time.time() - STARTED_AT, 2),
    )


@app.post("/cases/intake", response_model=CaseResponse, dependencies=[Depends(verify_api_key)])
def intake_case(req: IntakeRequest) -> CaseResponse:
    case_id = str(uuid.uuid4())
    payload = req.model_dump()
    payload["case_id"] = case_id

    db.save_case(case_id, payload)
    try:
        result = orchestrator.run_case(payload)
    except Exception as exc:
        db.audit_event(case_id, "workflow_failed", {"error": str(exc)})
        raise HTTPException(status_code=500, detail="Workflow execution failed") from exc
    return CaseResponse(**result)


@app.get("/cases/{case_id}", dependencies=[Depends(verify_api_key)])
def get_case(case_id: str):
    case = db.get_case(case_id)
    if case is None:
        raise HTTPException(status_code=404, detail="Case not found")
    return case


@app.get("/review-queue", dependencies=[Depends(verify_api_key)])
def review_queue():
    return {"pending_cases": get_pending_cases()}


@app.post("/cases/{case_id}/feedback", dependencies=[Depends(verify_api_key)])
def submit_feedback(case_id: str, feedback: FeedbackRequest):
    return record_feedback(case_id, feedback)
