from fastapi import FastAPI
from .config import print_cache_paths

app = FastAPI(title="LLM Train-Eval-Ship")


@app.on_event("startup")
async def on_startup():
    # Print shared cache paths at boot
    print_cache_paths()


@app.get("/healthz")
async def healthz():
    return {"status": "ok", "service": "llm-train-eval-ship"}
