# Deployment

This project is best deployed as a static GitHub Pages demo plus a local FastAPI backend for smoke testing.

## Public URLs

| Target | URL |
| --- | --- |
| GitHub Pages demo | `https://justin21523.github.io/LLM-train-eval-ship/` |
| Portfolio case study | `https://justin21523.github.io/zh-TW/projects/llm-train-eval-ship/` |

The repository name contains uppercase letters, so the GitHub Pages path is case-sensitive. Use `/LLM-train-eval-ship/`, not `/llm-train-eval-ship/`.

## GitHub Pages

The workflow in `.github/workflows/deploy-pages.yml` publishes `portfolio-web/` to the existing `gh-pages` branch used by this repository's legacy GitHub Pages settings:

```bash
git push origin main
gh run list --repo Justin21523/LLM-train-eval-ship --limit 5
```

The repository is currently configured for legacy branch-based Pages, so this workflow intentionally pushes the static demo to `gh-pages` instead of requiring a Pages source migration.

## Local static smoke

```bash
python3 -m http.server 4177 --directory portfolio-web
curl -I http://127.0.0.1:4177/
```

## Local backend smoke

```bash
uvicorn app.main:app --host 127.0.0.1 --port 8080
curl http://127.0.0.1:8080/healthz
curl http://127.0.0.1:8080/api/demo/pipeline/support-copilot-lora
```

## Docker static smoke

```bash
docker build -f docker/portfolio.Dockerfile -t llm-train-eval-ship-demo .
docker run --rm -p 8088:80 llm-train-eval-ship-demo
curl -I http://127.0.0.1:8088/
```

## Demo media

```bash
python3 scripts/capture_demo.py
```

Generated files:

- `docs/assets/cover.png`
- `docs/assets/screenshots/*.png`
- `docs/assets/demo/guided-demo.webm`
