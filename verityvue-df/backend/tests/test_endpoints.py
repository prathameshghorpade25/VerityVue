import pytest
from fastapi.testclient import TestClient
from app.main import app
from app.config import settings

client = TestClient(app)

def test_root():
	resp = client.get("/")
	assert resp.status_code == 200
	assert resp.json()["service"] == "verityvue"

def test_ingest_and_get():
	files = {"media": ("sample.txt", b"hello", "text/plain")}
	data = {
		"uploader": "tester",
		"timestamp": "2025-01-01T00:00:00Z",
		"text": "demo",
		"source": "test",
		"tags": "demo,unit",
	}
	resp = client.post("/ingest", data=data, files=files)
	assert resp.status_code == 200
	claim_id = resp.json()["claim_id"]

	resp_list = client.get("/claims")
	assert resp_list.status_code == 200
	assert any(c["id"] == claim_id for c in resp_list.json())

	resp_get = client.get(f"/claims/{claim_id}")
	assert resp_get.status_code == 200
	body = resp_get.json()
	assert body["id"] == claim_id


def test_demo_replay_and_publish():
	payload = {
		"items": [
			{
				"id": "T-001",
				"uploader": "demo_user",
				"timestamp": "2025-10-01T12:00:00Z",
				"text": "Demo politician synthetic clip",
				"source": "demo",
				"tags": ["politician"],
				"media": "demo_assets/benign_clip.mp4"
			}
		],
		"base_dir": "./demo"
	}
	# Create a small placeholder file for test
	import os
	os.makedirs('./demo/demo_assets', exist_ok=True)
	with open('./demo/demo_assets/benign_clip.mp4', 'wb') as f:
		f.write(b'abc')

	r = client.post('/demo/replay', json=payload)
	assert r.status_code == 200

	r2 = client.get('/claims/T-001')
	assert r2.status_code == 200
	body = r2.json()
	assert body['id'] == 'T-001'

	r3 = client.post('/claims/T-001/publish', headers={'Authorization': settings.moderator_token})
	assert r3.status_code == 200
	assert r3.json()['status'] == 'PUBLISHED'

