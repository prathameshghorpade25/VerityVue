from typing import List, Dict, Tuple
import os
from PIL import Image
import imagehash


class PHashIndex:
	def __init__(self):
		self.entries: List[Tuple[str, imagehash.ImageHash]] = []

	def add(self, path: str):
		try:
			with Image.open(path) as img:
				h = imagehash.phash(img)
				self.entries.append((path, h))
		except Exception:
			pass

	def build_from_dir(self, dir_path: str):
		for root, _, files in os.walk(dir_path):
			for f in files:
				if f.lower().endswith(('.jpg', '.jpeg', '.png', '.webp')):
					self.add(os.path.join(root, f))

	def search(self, query_path: str, top_k: int = 3) -> List[Dict]:
		try:
			with Image.open(query_path) as img:
				q = imagehash.phash(img)
		except Exception:
			return []
		results: List[Tuple[str, int]] = []
		for path, h in self.entries:
			dist = (h - q)
			results.append((path, dist))
		results.sort(key=lambda x: x[1])
		out: List[Dict] = []
		for path, dist in results[:top_k]:
			out.append({ 'source': 'phash', 'path_or_url': path, 'score': float(max(0, 64 - dist)) / 64.0 })
		return out
