from __future__ import annotations


def set_attrs(span, attrs: dict):
    for key, value in attrs.items():
        if value is not None:
            span.set_attribute(key, value)


def annotate_case_span(
    span,
    *,
    case_id: str,
    patient_id: str | None = None,
    clinic_id: str | None = None,
):
    set_attrs(
        span,
        {
            "case.id": case_id,
            "patient.id": patient_id,
            "clinic.id": clinic_id,
        },
    )
