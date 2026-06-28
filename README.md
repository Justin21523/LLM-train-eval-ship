# LLM Train-Eval-Ship

> A portfolio-ready, mock-safe LLM MLOps release console that demonstrates the path from dataset readiness to adapter tuning, automated evaluation, canary deployment, and rollback decisions.

![LLM Train-Eval-Ship cover](docs/assets/cover.png)

## Product Positioning

LLM Train-Eval-Ship is a **guided LLM release operations prototype**. Real large-model training usually needs GPUs, private datasets, model weights, and production serving infrastructure. This project focuses on the parts users can safely inspect in public: release gates, evaluation evidence, deployment decisions, shared model-cache governance, and rollback readiness.

| Area | What users can inspect | Status |
| --- | --- | --- |
| Backend service | FastAPI health check, demo scenarios, pipeline run, eval scorecard, deployment manifest | Complete |
| Mock-safe journey | Full release workflow without GPUs, API keys, model weights, or external services | Complete |
| Static product demo | GitHub Pages guided release console with the actual workflow on the first screen | Complete |
| Verification | pytest backend smoke tests, static smoke, Docker build, Playwright screenshots, WebM capture | Complete |
| Real model execution | LoRA/PEFT, DPO, vLLM/TGI production wiring | Roadmap |

## Public Entry Points

| Resource | URL |
| --- | --- |
| Interactive demo | https://justin21523.github.io/LLM-train-eval-ship/ |
| Portfolio case study | https://justin21523.github.io/zh-TW/projects/llm-train-eval-ship/ |
| GitHub repository | https://github.com/Justin21523/LLM-train-eval-ship |

## User Journey

1. Open the interactive demo and start the guided release walkthrough.
2. Choose one of three release candidates: Support Copilot LoRA, Policy DPO Safety Pass, or RAG Agent Regression Gate.
3. Follow the checkpoint lane: dataset readiness, adapter registration, AutoEval, and release decision.
4. Inspect the user decision panel to promote, hold, or roll back the adapter.
5. Review the README diagrams and API contracts to understand the system boundary.

```mermaid
flowchart LR
  A[Dataset upload] --> B[Schema and privacy gate]
  B --> C[Adapter tuning<br/>LoRA / PEFT / DPO]
  C --> D[AutoEval scorecard]
  D --> E{Release gate}
  E -->|Pass| F[Deploy through vLLM / TGI]
  E -->|Regression| G[Rollback previous adapter]
  F --> H[Canary traffic]
  H --> I[Promote, hold, or revert]
```

## System Architecture

```mermaid
flowchart TB
  subgraph Browser[Browser / GitHub Pages]
    UI[Guided release console]
    Capture[Playwright screenshots and WebM]
  end

  subgraph API[FastAPI mock-safe backend]
    Health[/GET /healthz/]
    Scenarios[/GET /api/demo/scenarios/]
    Pipeline[/GET /api/demo/pipeline/:id/]
    Eval[/GET /api/demo/eval-scorecard/]
    Deploy[/GET /api/demo/deployment-manifest/]
  end

  subgraph Ops[Production roadmap boundary]
    Cache[Shared Hugging Face cache paths]
    Train[LoRA / PEFT / DPO jobs]
    Serve[vLLM / TGI serving]
    Rollback[Canary and rollback policy]
  end

  UI --> Scenarios
  UI --> Pipeline
  Pipeline --> Eval
  Pipeline --> Deploy
  API --> Cache
  Cache -. roadmap .-> Train
  Train -. roadmap .-> Serve
  Serve -. roadmap .-> Rollback
  Capture --> UI
```

## Data And Control Flow

```mermaid
sequenceDiagram
  participant User as User
  participant Demo as Static release console
  participant API as FastAPI
  participant Store as Shared cache contract

  User->>Demo: choose release candidate
  Demo->>Demo: render deterministic workflow state
  User->>API: curl /api/demo/pipeline/support-copilot-lora
  API->>Store: read MODEL_STORE_ROOT / HF_HOME / TRANSFORMERS_CACHE / HF_HUB_CACHE
  API-->>User: scenario + checkpoints + scorecard + deployment manifest
```

## Module Organization

```mermaid
flowchart LR
  Root[repo root] --> App[app/]
  Root --> Tests[tests/]
  Root --> Web[portfolio-web/]
  Root --> Scripts[scripts/]
  Root --> Docs[docs/assets/]
  Root --> Docker[docker/]
  App --> Main[main.py FastAPI routes]
  App --> DemoData[demo_data.py deterministic scenarios]
  App --> Config[config.py cache path logging]
  Tests --> Smoke[test_demo_api.py]
  Web --> StaticUI[index.html + styles.css]
  Scripts --> Capture[capture_demo.py]
  Docs --> Media[cover, screenshots, WebM]
```

## Technology Stack

| Layer | Technology | Purpose |
| --- | --- | --- |
| Backend | Python, FastAPI, Uvicorn | Demo API, health check, pipeline contract |
| Test | pytest, FastAPI TestClient | Smoke tests |
| Static demo | HTML, CSS, Vanilla JS | GitHub Pages guided product journey |
| Media automation | Playwright, FFmpeg | Screenshot assets and WebM walkthrough |
| Deployment | GitHub Actions, GitHub Pages, Docker, Nginx | Static deployment and local container smoke |
| LLM roadmap | Hugging Face cache, LoRA/PEFT, DPO, vLLM, TGI | Production extension points |

```mermaid
mindmap
  root((LLM Train-Eval-Ship))
    Backend
      FastAPI
      Uvicorn
      pytest
    Product Demo
      GitHub Pages
      Guided user journey
      Playwright screenshots
      WebM walkthrough
    MLOps
      Shared HF cache
      AutoEval gate
      Canary deploy
      Rollback guard
    Roadmap
      LoRA / PEFT
      DPO
      vLLM
      TGI
```

## API Contract

| Method | Endpoint | Purpose |
| --- | --- | --- |
| GET | `/healthz` | Service status, demo mode, cache paths |
| GET | `/api/demo/scenarios` | Release candidates for the guided journey |
| GET | `/api/demo/pipeline/{scenario_id}` | Scenario, checkpoints, scorecard, and deployment manifest |
| GET | `/api/demo/eval-scorecard` | Mock AutoEval scorecard |
| GET | `/api/demo/deployment-manifest` | vLLM/TGI, canary, and rollback manifest |

## Local Backend

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt

export DEMO_MODE=mock
export MODEL_STORE_ROOT=/srv/model-store
export HF_HOME=/srv/model-store/hf-home
export TRANSFORMERS_CACHE=/srv/model-store/hf-cache
export HF_HUB_CACHE=/srv/model-store/hf-cache

uvicorn app.main:app --host 127.0.0.1 --port 8080
```

```bash
curl http://127.0.0.1:8080/healthz
curl http://127.0.0.1:8080/api/demo/pipeline/support-copilot-lora
```

## Static Demo

```bash
python3 -m http.server 4177 --directory portfolio-web
# open http://127.0.0.1:4177/
```

## Testing And Asset Capture

```bash
python3 -m pytest
python3 scripts/capture_demo.py
docker build -f docker/portfolio.Dockerfile -t llm-train-eval-ship-demo .
```

Generated assets:

| Path | Purpose |
| --- | --- |
| `docs/assets/cover.png` | README and portfolio cover |
| `docs/assets/screenshots/*.png` | Portfolio media gallery screenshots |
| `docs/assets/demo/guided-demo.webm` | Guided walkthrough video |

## Deployment Flow

```mermaid
flowchart LR
  Dev[Local repo] --> Test[pytest + static smoke + capture]
  Test --> Push[git push main]
  Push --> Actions[GitHub Actions]
  Actions --> Pages[GitHub Pages static demo]
  Pages --> Portfolio[Portfolio project page]
  Portfolio --> User[User opens public URLs]
```

## Demo Scenarios

| Scenario | Model | Method | Gate | User decision |
| --- | --- | --- | --- | --- |
| Support Copilot LoRA | Qwen2.5-7B-Instruct | LoRA / PEFT | Helpfulness + latency | Promote to 20% canary |
| Policy DPO Safety Pass | Mistral-7B-Instruct | DPO | Safety refusal + jailbreak probes | Hold for policy approval |
| RAG Agent Regression Gate | Llama-3.1-8B-Instruct | Adapter refresh | Citation grounding + latency | Roll back adapter |

## Risks And Honest Boundaries

| Risk | Explanation | Current handling |
| --- | --- | --- |
| No GPU or model weights | Real LoRA/DPO training cannot run in the public static demo | Deterministic mock-safe workflow |
| External services unavailable | Hugging Face or serving endpoints may need credentials and large resources | Demo does not depend on external services |
| Production serving not wired | vLLM/TGI integration is a contract boundary, not a live serving claim | UI and README label it as roadmap |
| Mock evaluation data | Scorecard demonstrates architecture, not real model quality | API returns `mode=mock` and `runtime=mock-safe` |

## What This Demonstrates

- Turning a thin FastAPI skeleton into a user-operable release journey.
- Handling common LLM demo constraints: GPUs, model weights, external services, secrets, and shared cache paths.
- Expressing production MLOps decisions through API contracts and mock-safe UI rather than a static marketing page.
- Producing reproducible screenshots and video assets with Playwright and FFmpeg.
