from contextlib import asynccontextmanager

from fastapi import FastAPI
from .demo_data import (
    DEMO_MODE,
    DEPLOYMENT_MANIFEST,
    EVAL_SCORECARD,
    SCENARIOS,
    cache_paths,
    pipeline_run,
)
from .config import print_cache_paths


@asynccontextmanager
async def lifespan(app: FastAPI):
    print_cache_paths()
    yield


app = FastAPI(
    title="LLM Train-Eval-Ship",
    description="Mock-safe train → eval → ship demo APIs for portfolio review.",
    version="1.0.0",
    lifespan=lifespan,
)


@app.get("/healthz")
async def healthz():
    return {
        "status": "ok",
        "service": "llm-train-eval-ship",
        "mode": DEMO_MODE,
        "demo_ready": True,
        "cache_paths": cache_paths(),
    }


@app.get("/api/demo/scenarios")
async def demo_scenarios():
    return {"mode": DEMO_MODE, "scenarios": SCENARIOS}


@app.get("/api/demo/pipeline/{scenario_id}")
async def demo_pipeline(scenario_id: str):
    return pipeline_run(scenario_id)


@app.get("/api/demo/eval-scorecard")
async def demo_eval_scorecard():
    return EVAL_SCORECARD


@app.get("/api/demo/deployment-manifest")
async def demo_deployment_manifest():
    return DEPLOYMENT_MANIFEST
