from __future__ import annotations

import os
from typing import Any


PROJECT_SLUG = "llm-train-eval-ship"
DEMO_MODE = os.getenv("DEMO_MODE", "mock").lower()


SCENARIOS: list[dict[str, Any]] = [
    {
        "id": "support-copilot-lora",
        "name": "Support Copilot LoRA",
        "audience": "Customer support AI team",
        "base_model": "Qwen2.5-7B-Instruct",
        "dataset": "12,480 anonymized support turns",
        "method": "LoRA / PEFT",
        "eval_suite": "Helpfulness, refusal safety, latency, regression",
        "deploy_engine": "vLLM",
        "risk": "Medium",
        "decision": "Promote to 20% canary",
    },
    {
        "id": "policy-dpo-safety",
        "name": "Policy DPO Safety Pass",
        "audience": "Trust and safety reviewers",
        "base_model": "Mistral-7B-Instruct",
        "dataset": "4,200 preference pairs",
        "method": "DPO",
        "eval_suite": "Safety refusal, jailbreak probes, answer quality",
        "deploy_engine": "TGI",
        "risk": "Low",
        "decision": "Ship after review sign-off",
    },
    {
        "id": "rag-agent-regression",
        "name": "RAG Agent Regression Gate",
        "audience": "Internal knowledge assistant owners",
        "base_model": "Llama-3.1-8B-Instruct",
        "dataset": "2,900 grounded QA samples",
        "method": "Adapter refresh",
        "eval_suite": "Citation grounding, tool allow-list, hallucination checks",
        "deploy_engine": "vLLM",
        "risk": "High",
        "decision": "Hold and rollback to previous adapter",
    },
]


STAGES: list[dict[str, Any]] = [
    {
        "id": "ingest",
        "label": "Dataset ingest",
        "status": "complete",
        "duration": "00:42",
        "summary": "Validated schema, privacy tags, and train/eval split manifest.",
    },
    {
        "id": "train",
        "label": "Fine-tune",
        "status": "complete",
        "duration": "18:30",
        "summary": "Mock-safe LoRA adapter artifact registered under MODEL_STORE_ROOT.",
    },
    {
        "id": "eval",
        "label": "Auto-eval",
        "status": "complete",
        "duration": "04:18",
        "summary": "Generated scorecard, regression deltas, and launch recommendation.",
    },
    {
        "id": "ship",
        "label": "Ship",
        "status": "ready",
        "duration": "01:05",
        "summary": "Prepared vLLM/TGI deployment manifest and canary rollback guard.",
    },
]


EVAL_SCORECARD: dict[str, Any] = {
    "overall": 92.4,
    "baseline": 87.1,
    "checks": [
        {"name": "Task helpfulness", "score": 94.8, "delta": "+5.7"},
        {"name": "Grounded answer rate", "score": 91.2, "delta": "+4.1"},
        {"name": "Safety refusal accuracy", "score": 96.5, "delta": "+2.8"},
        {"name": "P95 latency budget", "score": 86.9, "delta": "-1.5"},
    ],
    "recommendation": "Promote to canary when latency budget is accepted.",
}


DEPLOYMENT_MANIFEST: dict[str, Any] = {
    "runtime": "mock-safe",
    "serving": {
        "primary": "vLLM",
        "fallback": "TGI",
        "api_shape": "OpenAI-compatible / HF-compatible",
    },
    "canary": {
        "initial_traffic": "5%",
        "promotion_target": "20%",
        "rollback_trigger": "quality drop > 3% or p95 latency > 1.8s",
    },
    "artifacts": [
        "adapter.safetensors",
        "eval-scorecard.json",
        "deployment-manifest.json",
        "rollback-plan.md",
    ],
}


def cache_paths() -> dict[str, str | None]:
    return {
        "MODEL_STORE_ROOT": os.getenv("MODEL_STORE_ROOT"),
        "HF_HOME": os.getenv("HF_HOME"),
        "TRANSFORMERS_CACHE": os.getenv("TRANSFORMERS_CACHE"),
        "HF_HUB_CACHE": os.getenv("HF_HUB_CACHE"),
    }


def pipeline_run(scenario_id: str) -> dict[str, Any]:
    scenario = next((item for item in SCENARIOS if item["id"] == scenario_id), SCENARIOS[0])
    return {
        "mode": DEMO_MODE,
        "scenario": scenario,
        "stages": STAGES,
        "scorecard": EVAL_SCORECARD,
        "deployment": DEPLOYMENT_MANIFEST,
        "cache_paths": cache_paths(),
    }
