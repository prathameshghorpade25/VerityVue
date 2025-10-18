#!/usr/bin/env bash
set -euo pipefail
SCRIPT_DIR=$(cd "$(dirname "$0")" && pwd)
ROOT_DIR=$(cd "$SCRIPT_DIR/.." && pwd)

cd "$ROOT_DIR"

if [ ! -f .env ]; then
	cp .env.example .env
fi

docker compose up -d --build

python demo/replay_demo.py --file demo/demo_stream.json --host http://localhost:8000

echo "Open UI at http://localhost:5173"
