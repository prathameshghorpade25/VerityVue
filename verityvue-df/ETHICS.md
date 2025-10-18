# Ethics and Data Use

- Demo media are synthetic or consented, clearly labeled for evaluation only.
- No non-consensual intimate content is used or stored.
- A human-in-the-loop is required for publishing high-impact advisories.
- Data minimization: only essential demo artifacts are stored locally under `demo/` and `media/`.
- Deletion policy: remove all demo artifacts after the event using provided cleanup scripts.
- This prototype does not perform model training; it uses inference-only with pretrained checkpoints.
- Advisory text is generated via templates using only collected evidence; no hallucinated sources.
