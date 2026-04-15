from __future__ import annotations

import os
from dataclasses import dataclass


def _get_bool(name: str, default: bool = False) -> bool:
    value = os.getenv(name)
    if value is None:
        return default
    return value.strip().lower() in {"1", "true", "yes", "on"}


@dataclass(frozen=True)
class Settings:
    app_name: str = os.getenv("APP_NAME", "remote-ophthalmology-agentops-platform")
    app_env: str = os.getenv("APP_ENV", "development")
    log_level: str = os.getenv("LOG_LEVEL", "INFO")

    api_key: str = os.getenv("API_KEY", "dev-secret-key")
    db_path: str = os.getenv("DB_PATH", "cases.db")

    quality_endpoint: str = os.getenv("QUALITY_ENDPOINT", "quality-endpoint")
    disease_endpoint: str = os.getenv("DISEASE_ENDPOINT", "disease-endpoint")
    reasoning_endpoint: str = os.getenv("REASONING_ENDPOINT", "reasoning-endpoint")

    llm_base_url: str = os.getenv("LLM_BASE_URL", "http://localhost:1234/v1")
    llm_model_name: str = os.getenv("LLM_MODEL_NAME", "local-model")

    aws_region: str = os.getenv("AWS_REGION", "eu-central-1")
    use_mock_clients: bool = _get_bool("USE_MOCK_CLIENTS", True)
    use_llm_summary: bool = _get_bool("USE_LLM_SUMMARY", False)

    quality_pass_threshold: float = float(os.getenv("QUALITY_PASS_THRESHOLD", "0.70"))
    disease_confidence_threshold: float = float(os.getenv("DISEASE_CONFIDENCE_THRESHOLD", "0.60"))


settings = Settings()
