from __future__ import annotations


class SimpleLLMClient:
    def generate(self, prompt: str) -> str:
        return (
            "Clinician-facing summary: Findings are grounded on the image quality result, "
            "specialist disease classification, and retrieved patient background. "
            "Please review the case before issuing any final prescription."
        )
