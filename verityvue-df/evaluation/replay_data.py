import argparse
import json
import os
import time
import mimetypes
import requests


def main():
	parser = argparse.ArgumentParser()
	parser.add_argument('--file', required=True, help='Path to demo_stream.json')
	parser.add_argument('--host', default='http://localhost:8000')
	parser.add_argument('--delay', type=float, default=0.5)
	args = parser.parse_args()

	with open(args.file, 'r', encoding='utf-8') as f:
		items = json.load(f)

	for item in items:
		media_path = os.path.join(os.path.dirname(args.file), item['media'])
		mime, _ = mimetypes.guess_type(media_path)
		with open(media_path, 'rb') as fh:
			files = {'media': (os.path.basename(media_path), fh.read(), mime or 'application/octet-stream')}
			data = {
				'id': item['id'],
				'uploader': item['uploader'],
				'timestamp': item['timestamp'],
				'text': item.get('text', ''),
				'source': item.get('source', 'demo'),
				'tags': ','.join(item.get('tags', [])),
			}
			resp = requests.post(f"{args.host}/ingest", data=data, files=files, timeout=60)
			print(item['id'], resp.status_code, resp.text)
			time.sleep(args.delay)


if __name__ == '__main__':
	main()
