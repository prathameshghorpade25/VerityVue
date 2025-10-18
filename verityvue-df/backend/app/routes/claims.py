from fastapi import APIRouter, UploadFile, File, Form, HTTPException
from typing import Optional, Dict, Any, List
from ..state import CLAIMS, save_media_file, log_agent, AGENT_LOG, PHASH_INDEX
from uuid import uuid4
from ..ml.detector import detect_media, generate_heatmaps
from ..search.reverse_search_stub import search_near_duplicates
from ..verify.aggregator import aggregate
from ..frames import extract_frames_ffmpeg, is_video
import os

router = APIRouter()


@router.get('/health')
async def health():
	return { 'status': 'ok' }


@router.post("/ingest")
async def ingest(
	id: Optional[str] = Form(default=None),
	uploader: str = Form(...),
	timestamp: str = Form(...),
	text: str = Form(""),
	source: str = Form("demo"),
	tags: str = Form(""),
	media: UploadFile = File(...),
):
	claim_id = id or str(uuid4())
	content = await media.read()
	stored_path = save_media_file(claim_id, media.filename, content)
	frames: List[str] = []
	if is_video(stored_path):
		frames_dir = os.path.join(os.path.dirname(stored_path), 'frames')
		frames = extract_frames_ffmpeg(stored_path, frames_dir, fps=1, max_frames=12)
	# detection + heatmaps
	det = detect_media(stored_path, frames)
	heatmaps = []
	if frames and det.get('per_frame_scores'):
		heat_dir = os.path.join(os.path.dirname(stored_path), 'heatmap')
		heatmaps = generate_heatmaps(frames, det['per_frame_scores'], heat_dir)
	# reverse search: combine stub and phash
	stub_matches = search_near_duplicates(stored_path)
	phash_matches = []
	if frames:
		# use first frame
		phash_matches = PHASH_INDEX.search(frames[0])
	matches = []
	for m in stub_matches:
		matches.append({ 'source': 'stub', 'path_or_url': m['url'], 'title': m['title'], 'snippet': m['snippet'], 'score': 0.7 })
	for m in phash_matches:
		matches.append(m)
	# aggregation
	agg = aggregate({ 'clip_score': det['clip_score'] }, matches)
	CLAIMS[claim_id] = {
		"id": claim_id,
		"uploader": uploader,
		"timestamp": timestamp,
		"text": text,
		"source": source,
		"tags": tags.split(",") if tags else [],
		"media_path": stored_path,
		"status": "PROCESSED",
		"frames": frames,
		"heatmaps": heatmaps,
		"detection": det,
		"evidence": matches,
		"verdict": {"label": agg["verdict"], "confidence": agg["confidence"]},
		"advisory_preview": None,
	}
	log_agent("ingest_processed", {"claim_id": claim_id, "clip_score": det.get("clip_score"), "frames": len(frames), "heatmaps": len(heatmaps)})
	return {"claim_id": claim_id, "status": "PROCESSED"}


@router.get("/claims")
async def list_claims() -> List[Dict[str, Any]]:
	return [
		{
			"id": c["id"],
			"uploader": c["uploader"],
			"timestamp": c["timestamp"],
			"text": c["text"],
			"status": c["status"],
		}
		for c in CLAIMS.values()
	]


@router.get("/claims/{claim_id}")
async def get_claim(claim_id: str) -> Dict[str, Any]:
	if claim_id not in CLAIMS:
		raise HTTPException(status_code=404, detail="Not found")
	return CLAIMS[claim_id]


@router.get("/agent/logs")
async def agent_logs() -> List[Dict[str, Any]]:
	return AGENT_LOG
