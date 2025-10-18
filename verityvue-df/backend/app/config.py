import json
import os
from dataclasses import dataclass


@dataclass
class Settings:
	api_host: str = os.getenv("API_HOST", "0.0.0.0")
	api_port: int = int(os.getenv("API_PORT", "8000"))
	media_dir: str = os.getenv("MEDIA_DIR", "./media")
	moderator_token: str = os.getenv("MODERATOR_TOKEN", "demo-mod-token")
	thresholds_path: str = os.getenv("THRESHOLDS_PATH", "./config/thresholds.json")

	def load_thresholds(self):
		try:
			with open(self.thresholds_path, "r", encoding="utf-8") as f:
				return json.load(f)
		except Exception:
			return {"VIRALITY_THRESHOLD": 0.6, "SUSPICION_THRESHOLD": 0.7, "AUTO_PUBLISH_CONFIDENCE": 85}


settings = Settings()
THRESHOLDS = settings.load_thresholds()
