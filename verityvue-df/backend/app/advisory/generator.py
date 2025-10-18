from typing import Dict, Any, List

TEMPLATE_SYSTEM = (
	"You are a concise public advisory generator. You must not invent sources or facts. "
	"You will be given a verdict, a confidence score, and up to two evidence items (title, url, snippet). "
	"Produce a short advisory (max 45 words). The advisory must start with the verdict (e.g., \"Likely manipulated\", \"Unverified\", or \"Verified\"). "
	"Then include a one-sentence reason and cite the evidence by title and URL. Finally, recommend the next step (Escalate / Refer to official channel / No action needed)."
)


def build_advisory_input(claim_text: str, verdict: str, confidence: int, evidence: List[Dict[str, str]]):
	title1 = evidence[0]['title'] if len(evidence) > 0 else ''
	url1 = evidence[0]['url'] if len(evidence) > 0 else ''
	snippet1 = evidence[0]['snippet'] if len(evidence) > 0 else ''
	title2 = evidence[1]['title'] if len(evidence) > 1 else ''
	url2 = evidence[1]['url'] if len(evidence) > 1 else ''
	snippet2 = evidence[1]['snippet'] if len(evidence) > 1 else ''
	return (
		f"Claim: \"{claim_text}\"\n" 
		f"Verdict: \"{verdict}\" # SUPPORTS | REFUTES | UNVERIFIED\n" 
		f"Confidence: \"{confidence}\" # 0-100\n" 
		f"Evidence1: {title1} — {url1} — {snippet1}\n" 
		f"Evidence2: {title2} — {url2} — {snippet2}\n"
	)


def generate_advisory(claim_text: str, verdict_label: str, confidence: int, evidence: List[Dict[str, str]]) -> str:
	# Offline stub: deterministically format without LLM, respecting constraints
	prefix = {
		'REFUTES': 'Likely manipulated',
		'SUPPORTS': 'Verified',
		'UNVERIFIED': 'Unverified'
	}.get(verdict_label, 'Unverified')
	refs = []
	for ev in evidence[:2]:
		if ev.get('title') and ev.get('url'):
			refs.append(f"{ev['title']} ({ev['url']})")
	ref_text = '; '.join(refs) if refs else 'no corroborating sources'
	if prefix == 'Verified':
		next_step = 'No action needed'
	elif prefix == 'Likely manipulated':
		next_step = 'Escalate'
	else:
		next_step = 'Refer to official channel'
	reason = 'based on detection score and provenance checks'
	return f"{prefix}. {reason}. Evidence: {ref_text}. Confidence {confidence}%. {next_step}."
