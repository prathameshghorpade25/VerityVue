import os
import subprocess
from typing import List


def is_video(path: str) -> bool:
	return os.path.splitext(path)[1].lower() in {'.mp4', '.mov', '.mkv', '.avi'}


def extract_frames_ffmpeg(input_path: str, output_dir: str, fps: int = 1, max_frames: int = 12) -> List[str]:
	os.makedirs(output_dir, exist_ok=True)
	pattern = os.path.join(output_dir, 'frame_%04d.jpg')
	cmd = [
		'ffmpeg', '-y', '-i', input_path,
		'-vf', f'fps={fps}', '-frames:v', str(max_frames), pattern
	]
	try:
		subprocess.run(cmd, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
	except Exception:
		return []
	files = [os.path.join(output_dir, f) for f in os.listdir(output_dir) if f.lower().endswith('.jpg')]
	files.sort()
	return files
