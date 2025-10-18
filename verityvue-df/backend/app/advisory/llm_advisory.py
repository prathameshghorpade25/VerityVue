import os
from typing import List, Dict
from .generator import TEMPLATE_SYSTEM, build_advisory_input, generate_advisory as fallback_generate


def generate_with_llm(claim_text: str, verdict_label: str, confidence: int, evidence: List[Dict[str, str]]) -> str:
	provider = os.getenv('LLM_PROVIDER', 'openai')
	api_key = os.getenv('OPENAI_API_KEY')
	if provider == 'openai' and api_key:
		try:
			from openai import OpenAI
			client = OpenAI(api_key=api_key)
			prompt = build_advisory_input(claim_text, verdict_label, confidence, evidence)
			resp = client.chat.completions.create(
				model='gpt-4o-mini',
				messages=[
					{"role":"system","content":TEMPLATE_SYSTEM},
					{"role":"user","content":prompt}
				],
				max_tokens=80,
				temperature=0.2
			)
			text = resp.choices[0].message.content.strip()
			return text
		except Exception:
			pass
	# Fallback offline
	return fallback_generate(claim_text, verdict_label, confidence, evidence)
