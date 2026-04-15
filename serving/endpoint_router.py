from __future__ import annotations

from serving.inference_quality import local_quality_endpoint
from serving.inference_disease import local_disease_endpoint
from serving.inference_reasoning import local_reasoning_endpoint
from serving.inference_summary import local_summary_endpoint


class LocalEndpointRouter:
    def quality(self, payload: dict) -> dict:
        return local_quality_endpoint(payload)

    def disease(self, payload: dict) -> dict:
        return local_disease_endpoint(payload)

    def reasoning(self, payload: dict) -> dict:
        return local_reasoning_endpoint(payload)

    def summary(self, payload: dict) -> dict:
        return local_summary_endpoint(payload)
