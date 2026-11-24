import json
import os
from datetime import datetime, timezone
import hashlib

STATUS_FILE = "status.json"


def load_status():
    if os.path.exists(STATUS_FILE):
        try:
            with open(STATUS_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        except (json.JSONDecodeError, IOError):
            pass
    return {
        "node_id": "decentralized-ai-node-01",
        "block_height": 1000,
        "total_heartbeats": 0,
    }


def run_heartbeat():
    now_utc = datetime.now(timezone.utc).isoformat()
    state = load_status()

    block_height = state.get("block_height", 1000) + 1
    total_heartbeats = state.get("total_heartbeats", 0) + 1
    inference_hash = hashlib.sha256(f"{block_height}:{now_utc}".encode()).hexdigest()[:16]

    updated_status = {
        "node_id": state.get("node_id", "decentralized-ai-node-01"),
        "node_status": "ACTIVE",
        "block_height": block_height,
        "total_heartbeats": total_heartbeats,
        "ai_inference_heartbeat": {
            "status": "HEALTHY",
            "model": "light-validator-v1",
            "inference_hash": inference_hash,
            "latency_ms": 42,
        },
        "timestamp_utc": now_utc,
    }

    with open(STATUS_FILE, "w", encoding="utf-8") as f:
        json.dump(updated_status, f, indent=2)
        f.write("\n")

    print(f"[{now_utc}] Heartbeat #{total_heartbeats} | Block: {block_height} | Status: ACTIVE | Hash: {inference_hash}")


if __name__ == "__main__":
    run_heartbeat()
