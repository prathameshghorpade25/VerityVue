from typing import Dict, Any, List
from ..config import THRESHOLDS


def aggregate(det: Dict[str, Any], matches: List[Dict[str, Any]]) -> Dict[str, Any]:
	clip = det.get('clip_score') or 0.0
	suspicion = clip
	if suspicion >= THRESHOLDS.get('SUSPICION_THRESHOLD', 0.7):
		verdict = 'REFUTES'
		confidence = int(min(100, 60 + suspicion * 40))
	else:
		if matches:
			verdict = 'SUPPORTS'
			confidence = int(min(100, 50 + (1 - suspicion) * 40))
		else:
			verdict = 'UNVERIFIED'
			confidence = int(40 + (1 - abs(0.5 - suspicion)) * 20)

	top_evidence = matches[:2]
	return {
		"verdict": verdict,
		"confidence": confidence,
		"top_evidence": top_evidence,
	}
