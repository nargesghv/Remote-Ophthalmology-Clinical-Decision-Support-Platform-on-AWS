from __future__ import annotations

from monitoring.tracing.otel import setup_tracing
from monitoring.tracing.span_utils import annotate_case_span, set_attrs
from monitoring.metrics.workflow_metrics import WORKFLOW_ACTION_COUNT, WORKFLOW_LATENCY

tracer = setup_tracing("remote-ophthalmology-orchestrator")


def instrumented_workflow_stub(case_id: str, patient_id: str, clinic_id: str, action: str, latency: float):
    with tracer.start_as_current_span("case_workflow") as span:
        annotate_case_span(span, case_id=case_id, patient_id=patient_id, clinic_id=clinic_id)
        set_attrs(span, {"workflow.action": action})
        WORKFLOW_ACTION_COUNT.labels(action=action).inc()
        WORKFLOW_LATENCY.observe(latency)
        return {"instrumented": True}
