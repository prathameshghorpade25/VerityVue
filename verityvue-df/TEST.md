# VerityVue Demo Plan

Script (3–4 minutes):
1. Open frontend at http://localhost:5173. Show empty stream.
2. Run demo replay: `python demo/replay_demo.py --file demo/demo_stream.json --host http://localhost:8000`.
3. Refresh stream. Click each item (A: synthetic politician, B: individual, C: benign).
4. Show claim detail: detection score, evidence links, verdict/confidence.
5. For benign/control, click Publish (enter token `demo-mod-token`). Show advisory text.
6. For high-impact or low-confidence, click Escalate.
7. Open API logs at http://localhost:8000/docs (optional) and `/agent/logs` (if added later) to show decisions.

Fallback Screencast Instructions:
- Use any screen recorder (e.g., OBS). 1080p, 30fps.
- Record: starting services with `docker compose up`, replaying demo, browsing UI, publishing one advisory, escalating another.
- Save the file as `demo/verityvue_screencast.mp4`. Mention: synthetic/consented media only.
