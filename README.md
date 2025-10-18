# VerityVue

See the truth behind the frame.

VerityVue is an agentic AI system that detects, verifies, and triages suspicious images and videos (deepfakes and manipulated media). It produces provenance-rich forensic reports (evidence cards + confidence score), shows per-frame heatmaps, and routes high-risk or low-confidence items to a moderator dashboard for human review before publishing advisories to simulated channels.

---

## Table of contents

- Project status
- Features
- Architecture overview
- Quickstart (recommended: Docker)
- Quickstart (development without Docker)
- Demo & replay
- Tests
- Configuration & environment variables
- Contributing, ethics & license
- Troubleshooting

---

## Project status

Milestones 1–4 are implemented (skeleton, detection & reverse search, agentic planner, dashboard, tests, demo). The codebase contains:
- backend/ — FastAPI service, Celery tasks, ML stubs and verification aggregator
- frontend/ — React + Vite moderator dashboard
- demo/ — replay scripts and demo assets
- config/ — thresholds and other configuration
- docker-compose.yml — full stack with Redis, Postgres and worker

See the detailed milestone checklist in the repository for progress and decisions.

---

## Key features

- Ingest multipart image/video claims with metadata (POST /ingest)
- Deterministic detector + real detector wrapper producing per-frame scores
- Frame extraction (ffmpeg) and heatmap generation (OpenCV)
- Perceptual-hash reverse search for similar images
- Aggregator that returns verdicts (SUPPORTS / REFUTES / UNVERIFIED) with confidence (0–100) and ranked evidence
- Agentic planner using Celery + Redis (observe → plan → act)
- LLM-based advisory generator with strict templates (no hallucination)
- Moderator dashboard: list, inspector, playback, heatmap toggle, evidence cards, publish/escalate flows
- Publish endpoint that requires moderator token and logs simulated channel messages

---

## Architecture overview

- FastAPI backend exposes ingestion and claim endpoints and schedules verification tasks.
- Celery workers run detector, reverse search, and advisory tasks.
- Redis used for Celery broker/state; Postgres for persistent claim storage (configured in docker-compose).
- Frontend (React + Vite) queries the API for claim streams and inspectors.
- Demo replay script posts sample items to /ingest to exercise the end-to-end flow.

---

## Quickstart (Docker — recommended)

Prereqs:
- Docker Desktop (Windows) or Docker + Docker Compose
- Git

1) Copy env
```powershell
cp .env.example .env
```

2) Build and run the full stack:
```powershell
docker compose up --build
```
- Backend: http://localhost:8000
- Frontend: http://localhost:5173
- API docs: http://localhost:8000/docs

3) Seed demo stream (example PowerShell):
```powershell
# from repo root (Windows PowerShell)
python .\demo\replay_demo.py --file .\demo\demo_stream.json --host http://localhost:8000
```

Notes:
- Use `docker compose logs -f backend` or `docker compose logs -f worker` to follow agent runs.
- To rebuild after changes: `docker compose up --build --detach`.

---

## Quickstart (Without Docker — Windows)

Backend:
```powershell
cd backend
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
# API
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
# Worker (separate terminal)
celery -A app.agent.celery_app.celery worker --loglevel=INFO
```

Frontend:
```powershell
cd frontend
npm install
npm run dev
```

Set required env vars from `.env.example` before running services.

---

## Demo & replay

- demo/demo_stream.json contains example scenarios (politician, individual, benign).
- demo/replay_demo.py posts items to the API and demonstrates agentic flows (verify → advisory → moderator queue).

Example:
```powershell
python .\demo\replay_demo.py --file .\demo\demo_stream.json --host http://localhost:8000
```

---

## Tests

Backend:
```powershell
cd backend
pytest backend/tests -q
```

Frontend:
```powershell
cd frontend
npm test
```

CI configuration and coverage targets are included in the repo.

---

## Configuration & environment variables

Important files:
- .env.example — copy to .env and fill values
- config/thresholds.json — thresholds used by verifier & agent
- backend/app/config.py — runtime configuration loader

Typical env vars (defined in .env.example):
- DATABASE_URL
- REDIS_URL
- CELERY_BROKER_URL
- VITE_API_BASE (frontend)

Adjust thresholds in config/thresholds.json to tune verdict sensitivity and routing.

---

## Contributing, ethics & license

- See ETHICS.md for data policy, consent declarations, and human-in-loop rules.
- Follow the moderation and retention policies before running on real data.
- License: check LICENSE file in repository (or request license if missing).

---

## Troubleshooting

- ffmpeg errors: ensure ffmpeg is installed and on PATH (Windows: add ffmpeg\bin to PATH).
- Celery worker not processing tasks: confirm broker URL (Redis) and check `docker compose logs worker`.
- Frontend cannot reach API: verify VITE_API_BASE matches backend host (CORS enabled in backend).

---

If any section needs expansion (example commands, architecture diagram, or API reference), indicate which areas to prioritize and a concise set of additions will be prepared.
