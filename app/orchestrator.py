from __future__ import annotations

import time
import uuid
from typing import Any

from app import db
from app.agents import build_decision_explanation, build_structured_summary
from app.policy_engine import decide_workflow_action
from app.review_queue import enqueue_case
from app.schemas import CaseResponse


class WorkflowOrchestrator:
    def __init__(
        self,
        *,
        quality_client: Any,
        disease_client: Any,
        retrieval_client: Any,
        llm_client: Any | None = None,
        use_llm_summary: bool = False,
    ) -> None:
        self.quality_client = quality_client
        self.disease_client = disease_client
        self.retrieval_client = retrieval_client
        self.llm_client = llm_client
        self.use_llm_summary = use_llm_summary

    def run_case(self, payload: dict[str, Any]) -> dict[str, Any]:
        case_id = payload.get("case_id", str(uuid.uuid4()))
        payload["case_id"] = case_id
        start = time.time()

        db.audit_event(case_id, "workflow_started", {"patient_id": payload["patient_id"]})

        quality_result = self.quality_client.predict(payload)
        db.save_prediction(case_id, "quality", quality_result)
        db.save_workflow_state(case_id, "quality_completed", quality_result)

        if quality_result["label"] != "good":
            policy = decide_workflow_action(
                quality_label=quality_result["label"],
                quality_confidence=quality_result["confidence"],
                disease_label=None,
                disease_confidence=None,
                symptom_score=payload["symptom_score"],
                patient_background=None,
            )
            result = self._finalize(
                case_id=case_id,
                payload=payload,
                quality_result=quality_result,
                disease_result={
                    "disease_label": None,
                    "disease_name": None,
                    "severity": None,
                    "confidence": None,
                },
                patient_background={},
                policy=policy.model_dump(),
                started_at=start,
            )
            db.update_case_status(case_id, "retake_requested")
            return result

        disease_result = self.disease_client.predict(payload)
        db.save_prediction(case_id, "disease", disease_result)
        db.save_workflow_state(case_id, "disease_completed", disease_result)

        patient_background = self.retrieval_client.get_background(payload["patient_id"])
        db.save_workflow_state(case_id, "background_retrieved", patient_background)

        policy = decide_workflow_action(
            quality_label=quality_result["label"],
            quality_confidence=quality_result["confidence"],
            disease_label=disease_result["disease_label"],
            disease_confidence=disease_result["confidence"],
            symptom_score=payload["symptom_score"],
            patient_background=patient_background,
        )

        result = self._finalize(
            case_id=case_id,
            payload=payload,
            quality_result=quality_result,
            disease_result=disease_result,
            patient_background=patient_background,
            policy=policy.model_dump(),
            started_at=start,
        )

        if policy.requires_human_review:
            enqueue_case(case_id, policy.priority)

        db.update_case_status(case_id, "pending_review" if policy.requires_human_review else "completed")
        db.audit_event(case_id, "workflow_completed", {"action": policy.action})
        return result

    def _finalize(
        self,
        *,
        case_id: str,
        payload: dict[str, Any],
        quality_result: dict[str, Any],
        disease_result: dict[str, Any],
        patient_background: dict[str, Any],
        policy: dict[str, Any],
        started_at: float,
    ) -> dict[str, Any]:
        summary = build_structured_summary(
            quality_result=quality_result,
            disease_result=disease_result,
            patient_background=patient_background,
            policy_decision=policy,
            complaint=payload.get("complaint"),
        )
        explanation = build_decision_explanation(
            quality_result=quality_result,
            disease_result=disease_result,
            patient_background=patient_background,
            policy_decision=policy,
        )

        db.save_workflow_state(
            case_id,
            "finalized",
            {
                "summary": summary,
                "policy": policy,
            },
        )

        return CaseResponse(
            case_id=case_id,
            quality_status=quality_result["label"],
            disease_label=disease_result.get("disease_label"),
            disease_name=disease_result.get("disease_name"),
            severity=disease_result.get("severity"),
            confidence=disease_result.get("confidence"),
            action=policy["action"],
            priority=policy["priority"],
            requires_human_review=policy["requires_human_review"],
            summary=summary,
            explanation=explanation,
            workflow_latency_seconds=round(time.time() - started_at, 4),
        ).model_dump()
