from typing import Dict, Any, List
from datetime import datetime
from .config import settings
import os
import pathlib
from .search.phash_index import PHashIndex


CLAIMS: Dict[str, Dict[str, Any]] = {}
AGENT_LOG: List[Dict[str, Any]] = []
PHASH_INDEX = PHashIndex()


def init_storage():
	pathlib.Path(settings.media_dir).mkdir(parents=True, exist_ok=True)
	# build phash index once from demo corpus if present
	corpus_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), '..', 'demo', 'index_corpus')
	corpus_dir = os.path.abspath(corpus_dir)
	if os.path.isdir(corpus_dir) and not getattr(PHASH_INDEX, '_built', False):
		PHASH_INDEX.build_from_dir(corpus_dir)
		setattr(PHASH_INDEX, '_built', True)


def log_agent(event: str, meta: Dict[str, Any]):
	AGENT_LOG.append({
		"timestamp": datetime.utcnow().isoformat() + "Z",
		"event": event,
		"meta": meta,
	})


def save_media_file(claim_id: str, filename: str, content: bytes) -> str:
	init_storage()
	dir_path = os.path.join(settings.media_dir, claim_id)
	os.makedirs(dir_path, exist_ok=True)
	file_path = os.path.join(dir_path, filename)
	with open(file_path, "wb") as f:
		f.write(content)
	return file_path
