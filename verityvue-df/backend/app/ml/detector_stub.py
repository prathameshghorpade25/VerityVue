from typing import Dict, Any, List
import os


def is_video(path: str) -> bool:
	return os.path.splitext(path)[1].lower() in {'.mp4', '.mov', '.mkv', '.avi'}


def is_image(path: str) -> bool:
	return os.path.splitext(path)[1].lower() in {'.jpg', '.jpeg', '.png', '.webp'}


def run_detection(media_path: str) -> Dict[str, Any]:
	# Stub: produce deterministic pseudo-scores based on filename
	name = os.path.basename(media_path).lower()
	if is_video(media_path):
		frame_scores: List[float] = []
		for i in range(12):
			seed = sum(ord(ch) for ch in name) + i * 7
			frame_scores.append(((seed % 100) / 100.0) * 0.9)
		clip_score = sum(frame_scores) / len(frame_scores)
		return {"clip_score": round(clip_score, 3), "frame_scores": [round(s, 3) for s in frame_scores]}
	elif is_image(media_path):
		seed = sum(ord(ch) for ch in name)
		clip = ((seed % 100) / 100.0) * 0.9
		return {"clip_score": round(clip, 3), "frame_scores": []}
	else:
		return {"clip_score": 0.1, "frame_scores": []}
