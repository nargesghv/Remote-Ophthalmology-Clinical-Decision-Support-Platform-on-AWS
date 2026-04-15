from __future__ import annotations

from typing import Any, Literal, Optional

from pydantic import BaseModel, Field


WorkflowAction = Literal[
    "request_retake",
    "routine_review",
    "standard_clinician_review",
    "urgent_clinician_review",
]


class IntakeRequest(BaseModel):
    patient_id: str = Field(..., min_length=1)
    clinic_id: str = Field(..., min_length=1)
    age: int = Field(..., ge=0, le=120)
    symptom_score: int = Field(..., ge=0, le=10)
    image_b64: str = Field(..., min_length=16)
    complaint: Optional[str] = Field(default=None, max_length=1000)


class PolicyDecision(BaseModel):
    action: WorkflowAction
    reason: str
    priority: Literal["low", "medium", "high", "critical"]
    requires_human_review: bool


class CaseResponse(BaseModel):
    case_id: str
    quality_status: str
    disease_label: Optional[str] = None
    disease_name: Optional[str] = None
    severity: Optional[str] = None
    confidence: Optional[float] = None
    action: WorkflowAction
    priority: str
    requires_human_review: bool
    summary: str
    explanation: dict[str, Any]
    workflow_latency_seconds: float


class FeedbackRequest(BaseModel):
    doctor_id: str = Field(..., min_length=1)
    approved: bool
    corrected_disease_label: Optional[str] = None
    corrected_action: Optional[WorkflowAction] = None
    override_reason: Optional[str] = None
    notes: Optional[str] = None


class HealthResponse(BaseModel):
    status: Literal["ok"]
    service: str
    uptime_seconds: float
