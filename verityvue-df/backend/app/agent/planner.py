from .celery_app import celery
from ..state import CLAIMS, log_agent
from ..verify.aggregator import aggregate
from ..ml.detector import detect_media
from ..search.reverse_search_stub import search_near_duplicates
from ..config import THRESHOLDS
from ..frames import extract_frames_ffmpeg, is_video
import os


def compute_virality_score(claim: dict) -> float:
	base = 0.2
	if any(t in (claim.get('tags') or []) for t in ['politician', 'breaking']):
		base += 0.3
	if len(claim.get('text') or '') > 40:
		base += 0.1
	return min(1.0, base)


@celery.task(name='verify_task')
def verify_task(claim_id: str):
	claim = CLAIMS.get(claim_id)
	if not claim:
		return None
	frames = []
	if is_video(claim['media_path']):
		frames_dir = os.path.join(os.path.dirname(claim['media_path']), 'frames')
		frames = extract_frames_ffmpeg(claim['media_path'], frames_dir, fps=1, max_frames=12)
	det = detect_media(claim['media_path'], frames)
	CLAIMS[claim_id]['frames'] = frames
	CLAIMS[claim_id]['detection'] = det
	log_agent('observed', { 'claim_id': claim_id, 'frames': len(frames) })
	return det


@celery.task(name='reverse_search_task')
def reverse_search_task(claim_id: str):
	claim = CLAIMS.get(claim_id)
	if not claim:
		return []
	stub = search_near_duplicates(claim['media_path'])
	matches = [{ 'source': 'stub', 'path_or_url': m['url'], 'title': m['title'], 'snippet': m['snippet'], 'score': 0.7 } for m in stub]
	CLAIMS[claim_id]['evidence'] = matches
	log_agent('planned', { 'claim_id': claim_id, 'steps': ['verify', 'reverse_search'] })
	return matches


@celery.task(name='advisory_task')
def advisory_task(claim_id: str):
	claim = CLAIMS.get(claim_id)
	if not claim:
		return None
	det = claim.get('detection') or {'clip_score': 0.0}
	matches = claim.get('evidence') or []
	agg = aggregate({ 'clip_score': det.get('clip_score') or 0.0 }, matches)
	CLAIMS[claim_id]['verdict'] = { 'label': agg['verdict'], 'confidence': agg['confidence'] }
	CLAIMS[claim_id]['status'] = 'REVIEW_REQUIRED'
	log_agent('acted', { 'claim_id': claim_id, 'verdict': agg['verdict'], 'confidence': agg['confidence'] })
	log_agent('result', { 'claim_id': claim_id })
	return agg


@celery.task(name='plan_and_act')
def plan_and_act(claim_id: str):
	# Orchestrate sequentially for demo simplicity
	verify_task.delay(claim_id)
	reverse_search_task.delay(claim_id)
	advisory_task.delay(claim_id)
	return True
