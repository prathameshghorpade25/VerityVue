from typing import Dict, Any, List
import os
import cv2
import numpy as np
from .detector_stub import run_detection as fallback_detect


def normalize_score(score: float) -> float:
	if score is None:
		return 0.0
	# clamp to [0,1]
	return max(0.0, min(1.0, float(score)))


def detect_media(media_path: str, frame_paths: List[str]) -> Dict[str, Any]:
	# For images, use fallback clip score; for videos, per-frame from fallback then normalize to [0,1]
	res = fallback_detect(media_path)
	clip = normalize_score(res.get('clip_score') or 0.0)
	per_frame = res.get('frame_scores') or []
	per_frame = [normalize_score(s) for s in per_frame]
	return { 'clip_score': round(clip, 3), 'per_frame_scores': [round(x, 3) for x in per_frame] }


def generate_heatmaps(frame_paths: List[str], per_frame_scores: List[float], out_dir: str) -> List[str]:
	os.makedirs(out_dir, exist_ok=True)
	heatmap_paths: List[str] = []
	for idx, fp in enumerate(frame_paths):
		if idx >= len(per_frame_scores):
			break
		try:
			img = cv2.imread(fp)
			if img is None:
				continue
			h, w = img.shape[:2]
			score = per_frame_scores[idx]
			# Create a simple heatmap: red intensity by score
			heat = np.zeros((h, w, 3), dtype=np.uint8)
			heat[:, :, 2] = int(255 * score)  # red channel
			heat = cv2.applyColorMap(heat, cv2.COLORMAP_JET)
			blend = cv2.addWeighted(img, 0.6, heat, 0.4, 0)
			out_path = os.path.join(out_dir, f"frame_{idx+1:04d}_heatmap.png")
			cv2.imwrite(out_path, blend)
			heatmap_paths.append(out_path)
		except Exception:
			continue
	return heatmap_paths
