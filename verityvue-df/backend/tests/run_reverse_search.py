import sys
import json
import os
from PIL import Image, ImageDraw
from app.search.phash_index import PHashIndex


def ensure_corpus(dir_path: str):
	if not os.path.isdir(dir_path):
		os.makedirs(dir_path, exist_ok=True)
		# create simple images
		for i in range(3):
			img = Image.new('RGB', (64, 64), color=(i*40, 100, 150))
			d = ImageDraw.Draw(img)
			d.text((5, 25), f"{i}", fill=(255, 255, 255))
			img.save(os.path.join(dir_path, f'sample_{i}.jpg'), 'JPEG')


if __name__ == '__main__':
	if len(sys.argv) < 2:
		print('usage: python run_reverse_search.py <image_path>')
		sys.exit(1)
	img_path = sys.argv[1]
	corpus_dir = './demo/index_corpus'
	ensure_corpus(corpus_dir)
	idx = PHashIndex()
	idx.build_from_dir(corpus_dir)
	out = idx.search(img_path)
	print(json.dumps(out))
