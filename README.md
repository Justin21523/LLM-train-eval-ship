# LLM Train-Eval-Ship

A portfolio-ready, one-click pipeline to **fine-tune LLMs**, **auto-evaluate**, and **deploy** via **vLLM** or **TGI** with **shared model caches**.
Includes FastAPI skeleton, cache path prints, and ready-to-extend hooks for LoRA/DPO, RAG/Agent, and HIL feedback.

## Key Features
- **One-click flow**: dataset upload → fine-tune → auto-eval → deploy.
- **Deploy engines**: vLLM or TGI (OpenAI/HF compatible).
- **Shared caches**: `HF_HOME / TRANSFORMERS_CACHE / HF_HUB_CACHE` to avoid re-downloading.
- **Canary & rollback** (roadmap): traffic shift and safe fallback.
- **Extensible**: LoRA/PEFT, DPO, RAG tools whitelist, AutoEval dashboards.

## Quickstart
```bash
python3 -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
export MODEL_STORE_ROOT=/srv/model-store
export HF_HOME=/srv/model-store/hf-home
export TRANSFORMERS_CACHE=/srv/model-store/hf-cache
export HF_HUB_CACHE=/srv/model-store/hf-cache
uvicorn app.main:app --host 0.0.0.0 --port 8080
# open http://localhost:8080/healthz
