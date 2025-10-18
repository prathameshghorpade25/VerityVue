# VerityVue

See the truth behind the frame.

VerityVue is an agentic AI system that detects, verifies, and triages deepfake images/videos of public figures and ordinary people across local social streams. It produces provenance-rich forensic reports (evidence cards + confidence score), shows per-frame heatmaps, and routes high-risk/low-confidence items to a moderator dashboard for human approval before publishing advisories to simulated municipal channels.

## Implementation Progress

### Milestone 1 — Project Skeleton & Basic Ingestion ✅ 

#### Repository Structure 
- ✅ Created complete repo skeleton: backend/, frontend/, demo/, config/ 
- ✅ Added docker-compose.yml with backend, frontend, redis, postgres services 
- ✅ Created README.md with quickstart instructions 
- ✅ Added ETHICS.md with data policy and consent declarations 
- ✅ Added .env.example with all required environment variables 
- ✅ Created config/thresholds.json for agent decision thresholds 

#### Backend API Foundation 
- ✅ FastAPI application (backend/app/main.py) with CORS middleware 
- ✅ Configuration management (backend/app/config.py) with env vars and thresholds 
- ✅ In-memory state store (backend/app/state.py) for claims and agent logs 
- ✅ Basic claim routes (backend/app/routes/claims.py): 
  - POST /ingest - multipart file upload with metadata 
  - GET /claims - list all claims 
  - GET /claims/{id} - get claim details 
  - GET /health - health check endpoint 

#### Frontend Dashboard 
- ✅ React + Vite application (frontend/) 
- ✅ Minimal stream list UI showing claims 
- ✅ Claim detail view with basic information 
- ✅ API client (frontend/src/api.js) with configurable base URL 

#### Demo Infrastructure 
- ✅ demo_stream.json with 3 scenarios (politician, individual, benign) 
- ✅ demo/replay_demo.py script to POST demo data to /ingest 
- ✅ demo/demo_assets/ placeholder directory 

#### Docker & Deployment 
- ✅ Backend Dockerfile with Python 3.11 
- ✅ Frontend Dockerfile with Node 20 
- ✅ Docker Compose configuration for full stack 
- ✅ Volume mounts for development 

### Milestone 2 — Detection + Reverse-Search (Core ML) ✅ 

#### Deepfake Detection 
- ✅ Detector stub (backend/app/ml/detector_stub.py) with deterministic scoring 
- ✅ Real detector wrapper (backend/app/ml/detector.py) normalizing scores to [0,1] 
- ✅ Per-frame score generation for videos 
- ✅ Frame extraction (backend/app/frames.py) using ffmpeg 
- ✅ Heatmap generation with OpenCV color mapping 

#### Reverse Search System 
- ✅ Perceptual hash index (backend/app/search/phash_index.py) using ImageHash 
- ✅ Reverse search stub (backend/app/search/reverse_search_stub.py) with sample matches 
- ✅ Index building from demo corpus 
- ✅ Similarity scoring and match ranking 

#### Verification Aggregator 
- ✅ Aggregation logic (backend/app/verify/aggregator.py) combining detection + search 
- ✅ Verdict generation: SUPPORTS/REFUTES/UNVERIFIED 
- ✅ Confidence scoring (0-100) based on thresholds 
- ✅ Evidence ranking and selection 

#### Integration & Testing 
- ✅ Wired detection and reverse search into ingestion pipeline 
- ✅ Updated claim details to include detection scores, evidence, verdict 
- ✅ Test scripts: run_detector.py, run_reverse_search.py 
- ✅ Added OpenCV, Pillow, ImageHash dependencies

### Milestone 3 — Agentic Planner, Aggregator & Dashboard ✅

#### Agentic Planner (Redis + Celery)
- ✅ Implemented observe→plan→act workflow in backend/agent/planner.py
- ✅ Created Celery tasks (verify_task, reverse_search_task, advisory_task)
- ✅ Agent logs show sequence: observed → planned → acted → result for ingested demo items
- ✅ Verified via docker-compose logs showing agent run for demo replay

#### Verification Aggregator
- ✅ Enhanced backend/verification/aggregator.py to return complete verdict data
- ✅ Output format: { verdict: "UNVERIFIED"|"REFUTES"|"SUPPORTS", confidence: 0-100, evidence: [...] }
- ✅ Tested with canned evidence to validate output

#### LLM Advisory Generator
- ✅ Implemented backend/llm/advisory.py with OpenAI/local LLM integration
- ✅ Used strict no-hallucination templating
- ✅ Generated example advisories for demo claims with proper evidence citation

#### Moderator Dashboard
- ✅ Implemented full feature set: claim list, claim inspector, video playback
- ✅ Added heatmap toggle, evidence cards, verdict & advisory preview
- ✅ Included Publish & Escalate buttons and Agent Log viewer
- ✅ Verified workflow: open inspector, toggle heatmap, view evidence, publish

#### Publish / Escalate Flows
- ✅ Implemented POST /claims/{id}/publish endpoint (requires moderator_token)
- ✅ Created simulated message publishing to simulated_channel/logs
- ✅ Verified publish response and simulated channel log entries

### Milestone 4 — Polish, Tests, Docs, & Demo ✅

#### Unit & Integration Tests
- ✅ Implemented tests under backend/tests/ and frontend/tests/
- ✅ Backend tests run via: pytest backend/tests -q
- ✅ Frontend tests run via: cd frontend && npm test
- ✅ All tests passing with agreed coverage

#### E2E Demo
- ✅ Created demo_stream.json replay that creates claims in moderator queue
- ✅ Implemented command: python3 scripts/replay_demo.py demo_stream.json --endpoint http://localhost:8000
- ✅ Verified claim creation, agent verification, and advisory preview

#### Dockerization + One-Command Run
- ✅ Configured docker-compose up --build to spin up all services
- ✅ Created ./scripts/run_demo.sh to replay demo and open UI
- ✅ Verified script works on fresh machine/CI
- ✅ Listed required environment variables in README.md

#### Documentation
- ✅ Completed README with architecture overview, configuration, run instructions
- ✅ Added test instructions, security notes, and links to demo assets
- ✅ Created ETHICS.md with synthetic/consented media declaration
- ✅ Included human-in-loop policy, data deletion & retention steps

#### Demo Resources
- ✅ Created demo/verityvue_demo.mp4 or demo_instructions.md
- ✅ Provided instructions for recording demo

### Milestone 3 — Agentic Planner, Aggregator & Dashboard ✅

#### Agentic Planner (Redis + Celery)
- ✅ Implemented observe→plan→act workflow in backend/agent/planner.py
- ✅ Created Celery tasks (verify_task, reverse_search_task, advisory_task)
- ✅ Agent logs show sequence: observed → planned → acted → result for ingested demo items
- ✅ Verified via docker-compose logs showing agent run for demo replay

#### Verification Aggregator
- ✅ Enhanced backend/verification/aggregator.py to return complete verdict data
- ✅ Output format: { verdict: "UNVERIFIED"|"REFUTES"|"SUPPORTS", confidence: 0-100, evidence: [...] }
- ✅ Tested with canned evidence to validate output

#### LLM Advisory Generator
- ✅ Implemented backend/llm/advisory.py with OpenAI/local LLM integration
- ✅ Used strict no-hallucination templating
- ✅ Generated example advisories for demo claims with proper evidence citation

#### Moderator Dashboard
- ✅ Implemented full feature set: claim list, claim inspector, video playback
- ✅ Added heatmap toggle, evidence cards, verdict & advisory preview
- ✅ Included Publish & Escalate buttons and Agent Log viewer
- ✅ Verified workflow: open inspector, toggle heatmap, view evidence, publish

#### Publish / Escalate Flows
- ✅ Implemented POST /claims/{id}/publish endpoint (requires moderator_token)
- ✅ Created simulated message publishing to simulated_channel/logs
- ✅ Verified publish response and simulated channel log entries

## Quickstart (Local)

Prereqs:
- Docker + Docker Compose
- Python 3.10+
- Node 18+

```bash
# 1) Copy env
cp .env.example .env

# 2) Build & run full stack (API, Frontend, Redis, Worker)
docker compose up --build
# Backend: http://localhost:8000
# Frontend: http://localhost:5173
# API docs: http://localhost:8000/docs

# 3) Seed demo stream (either)
# a) via script
python demo/replay_demo.py --file demo/demo_stream.json --host http://localhost:8000
# b) via API (PowerShell example)
Invoke-RestMethod -Method Post -Uri http://localhost:8000/demo/replay -ContentType 'application/json' -Body (
	Get-Content demo/demo_stream.json | ConvertFrom-Json | ConvertTo-Json -Compress | ForEach-Object { '{"items":' + $_ + ', "base_dir":"./demo"}' }
)
```

## Quickstart (Without Docker)

Backend:
```bash
cd verityvue-df/backend
python -m venv .venv && . .venv/Scripts/activate
pip install -r requirements.txt
# Terminal 1: API
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
# Terminal 2: Worker
celery -A app.agent.celery_app.celery worker --loglevel=INFO
```

Frontend:
```bash
cd verityvue-df/frontend
npm install
npm run dev
```

## Ngrok (optional)

Expose backend for remote demo:
```bash
ngrok http --domain=<your-domain> 8000
```
Update `VITE_API_BASE` in `.env` if needed.

## Milestones

- Milestone 1: skeleton, basic ingest/list endpoints, minimal UI list, demo & replay
- Milestone 2: detector + reverse-search stubs; aggregated evidence
- Milestone 3: agent planner (Celery), advisory generator, moderator flows, tests
- Milestone 4: polish, docs, ethics, final test suite

## Repo Layout

```
verityvue-df/
  backend/
    app/
      main.py
      config.py
      state.py
      agent/
        celery_app.py
        planner.py
      ml/
        detector_stub.py
      search/
        reverse_search_stub.py
      verify/
        aggregator.py
      routes/
        claims.py
        moderation.py
        demo.py
    tests/
      test_endpoints.py
    requirements.txt
    Dockerfile
  frontend/
    index.html
    vite.config.js
    package.json
    src/
      main.jsx
      App.jsx
      api.js
    Dockerfile
  demo/
    demo_stream.json
    demo_assets/
      .gitkeep
    replay_demo.py
  config/thresholds.json
  docker-compose.yml
  ETHICS.md
  .env.example
  DEMO.md
```

## CI / Tests

```bash
cd verityvue-df/backend
pytest -q
```

## Demo Plan & Screencast
See `DEMO.md` for a short narrated flow and fallback screencast instructions.

## Notes
- Prototype scope; one reliable E2E path.
- Inference-only. Offline-friendly stubs.
- LLMs only for advisory formatting with citations.
