from fastapi.testclient import TestClient

from app.main import app


client = TestClient(app)


def test_healthz_reports_demo_ready():
    response = client.get("/healthz")

    assert response.status_code == 200
    payload = response.json()
    assert payload["status"] == "ok"
    assert payload["demo_ready"] is True
    assert payload["mode"] == "mock"
    assert "cache_paths" in payload


def test_demo_scenarios_are_available():
    response = client.get("/api/demo/scenarios")

    assert response.status_code == 200
    scenarios = response.json()["scenarios"]
    assert len(scenarios) >= 3
    assert scenarios[0]["id"] == "support-copilot-lora"


def test_pipeline_run_contains_interview_ready_sections():
    response = client.get("/api/demo/pipeline/support-copilot-lora")

    assert response.status_code == 200
    payload = response.json()
    assert payload["scenario"]["name"] == "Support Copilot LoRA"
    assert len(payload["stages"]) == 4
    assert payload["scorecard"]["overall"] > payload["scorecard"]["baseline"]
    assert payload["deployment"]["canary"]["initial_traffic"] == "5%"


def test_eval_and_deployment_endpoints():
    scorecard = client.get("/api/demo/eval-scorecard")
    manifest = client.get("/api/demo/deployment-manifest")

    assert scorecard.status_code == 200
    assert manifest.status_code == 200
    assert scorecard.json()["recommendation"]
    assert manifest.json()["runtime"] == "mock-safe"
