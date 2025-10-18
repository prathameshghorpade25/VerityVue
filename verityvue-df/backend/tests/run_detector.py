import sys
import json
from app.ml.detector import detect_media

if __name__ == '__main__':
	if len(sys.argv) < 2:
		print('usage: python run_detector.py <media_path>')
		sys.exit(1)
	media_path = sys.argv[1]
	result = detect_media(media_path, [])
	print(json.dumps(result))
