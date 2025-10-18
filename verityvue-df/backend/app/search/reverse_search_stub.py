from typing import List, Dict
import os


SAMPLE_INDEX = [
	{"title": "Local News Article", "url": "https://example.local/news/123", "snippet": "Context about prior speech."},
	{"title": "Public Statement Archive", "url": "https://example.local/archive/mayor", "snippet": "Official statements collection."},
	{"title": "Community Event Video", "url": "https://example.local/video/abc", "snippet": "Benign community clip."}
]


def search_near_duplicates(media_path: str) -> List[Dict]:
	name = os.path.basename(media_path).lower()
	if 'politician' in name:
		return [SAMPLE_INDEX[0], SAMPLE_INDEX[1]]
	if 'individual' in name:
		return [SAMPLE_INDEX[1]]
	if 'benign' in name:
		return [SAMPLE_INDEX[2]]
	return SAMPLE_INDEX[:1]
