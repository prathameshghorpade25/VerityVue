from fastapi import APIRouter, HTTPException, Header
from typing import Optional
from ..state import CLAIMS, log_agent
from ..config import settings
from ..advisory.generator import generate_advisory
from ..advisory.llm_advisory import generate_with_llm

router = APIRouter()

SIMULATED_CHANNEL: list[dict] = []


def require_mod(token: Optional[str]):
	if token != settings.moderator_token:
		raise HTTPException(status_code=403, detail='Forbidden')


@router.post('/claims/{claim_id}/publish')
async def publish_advisory(claim_id: str, authorization: Optional[str] = Header(default=None)):
	require_mod(authorization)
	claim = CLAIMS.get(claim_id)
	if not claim:
		raise HTTPException(status_code=404, detail='Not found')
	verdict = claim.get('verdict') or {}
	# Try LLM, fallback to template formatter
	advisory = generate_with_llm(claim.get('text', ''), verdict.get('label') or 'UNVERIFIED', int(verdict.get('confidence') or 0), claim.get('evidence') or [])
	if not advisory:
		advisory = generate_advisory(claim.get('text', ''), verdict.get('label') or 'UNVERIFIED', int(verdict.get('confidence') or 0), claim.get('evidence') or [])
	CLAIMS[claim_id]['advisory_preview'] = advisory
	CLAIMS[claim_id]['status'] = 'PUBLISHED'
	entry = { 'claim_id': claim_id, 'advisory': advisory, 'evidence': claim.get('evidence') or [] }
	SIMULATED_CHANNEL.append(entry)
	log_agent('published', { 'claim_id': claim_id })
	return { 'status': 'PUBLISHED', 'advisory': advisory }


@router.post('/claims/{claim_id}/escalate')
async def escalate_claim(claim_id: str, authorization: Optional[str] = Header(default=None)):
	require_mod(authorization)
	if claim_id not in CLAIMS:
		raise HTTPException(status_code=404, detail='Not found')
	CLAIMS[claim_id]['status'] = 'ESCALATED'
	log_agent('escalated', { 'claim_id': claim_id })
	return { 'status': 'ESCALATED' }


@router.get('/simulated_channel/logs')
async def get_channel_logs():
	return SIMULATED_CHANNEL
