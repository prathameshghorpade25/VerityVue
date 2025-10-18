from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List, Optional, Dict, Any
import os
from ..state import save_media_file, CLAIMS, log_agent
from ..ml.detector_stub import run_detection
from ..search.reverse_search_stub import search_near_duplicates
from ..verify.aggregator import aggregate

router = APIRouter()


class DemoItem(BaseModel):
	id: str
	uploader: str
	timestamp: str
	text: Optional[str] = ''
	source: Optional[str] = 'demo'
	tags: Optional[List[str]] = []
	media: str
	virality: Optional[Dict[str, Any]] = None


class ReplayRequest(BaseModel):
	items: List[DemoItem]
	base_dir: Optional[str] = None


@router.post('/demo/replay')
async def demo_replay(body: ReplayRequest):
	base_dir = body.base_dir or './demo'
	created = []
	for item in body.items:
		media_path = item.media
		if not os.path.isabs(media_path):
			media_path = os.path.join(base_dir, media_path)
		if not os.path.exists(media_path):
			raise HTTPException(status_code=400, detail=f"Missing media: {media_path}")
		with open(media_path, 'rb') as f:
			content = f.read()
		stored_path = save_media_file(item.id, os.path.basename(media_path), content)
		detection = run_detection(stored_path)
		matches = search_near_duplicates(stored_path)
		agg = aggregate(detection, matches)
		CLAIMS[item.id] = {
			"id": item.id,
			"uploader": item.uploader,
			"timestamp": item.timestamp,
			"text": item.text or '',
			"source": item.source or 'demo',
			"tags": item.tags or [],
			"media_path": stored_path,
			"status": "PROCESSED",
			"frames": [],
			"detection": detection,
			"evidence": matches,
			"verdict": {"label": agg["verdict"], "confidence": agg["confidence"]},
			"advisory_preview": None,
		}
		log_agent('replay_ingest', { 'claim_id': item.id })
		created.append(item.id)
	return { 'created': created, 'count': len(created) }
