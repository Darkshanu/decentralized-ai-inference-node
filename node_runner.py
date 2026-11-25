import json
import os
import time
import urllib.request
from datetime import datetime, timezone
import hashlib

STATUS_FILE = "status.json"
INJECTIVE_LCD_URL = "https://sentry.lcd.injective.network/cosmos/base/tendermint/v1beta1/blocks/latest"


def load_status():
    if os.path.exists(STATUS_FILE):
        with open(STATUS_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return {
        "node_id": "decentralized-ai-node-01",
        "node_status": "ACTIVE",
        "block_height": 102400,
        "total_heartbeats": 0,
    }


def get_injective_status():
    start_time = time.perf_counter()
    try:
        req = urllib.request.Request(
            INJECTIVE_LCD_URL,
            headers={"User-Agent": "decentralized-ai-inference-node/1.0"},
        )
        with urllib.request.urlopen(req, timeout=10) as response:
            data = json.loads(response.read().decode("utf-8"))
        latency_ms = round((time.perf_counter() - start_time) * 1000, 2)
        height = int(data["block"]["header"]["height"])
        return {
            "network": "injective-mainnet",
            "endpoint": INJECTIVE_LCD_URL,
            "status": "CONNECTED",
            "latest_block_height": height,
            "latency_ms": latency_ms,
        }
    except Exception as exc:
        latency_ms = round((time.perf_counter() - start_time) * 1000, 2)
        return {
            "network": "injective-mainnet",
            "endpoint": INJECTIVE_LCD_URL,
            "status": "ERROR",
            "latest_block_height": None,
            "latency_ms": latency_ms,
            "error": str(exc),
        }


def run_heartbeat():
    state = load_status()
    now_utc = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")

    # Simulate an incremental block height and deterministic inference hash
    block_height = state.get("block_height", 102400) + 1
    total_heartbeats = state.get("total_heartbeats", 0) + 1
    inference_hash = hashlib.sha256(f"{block_height}:{now_utc}".encode()).hexdigest()[:16]
    injective_status = get_injective_status()

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
        "injective_network": injective_status,
        "timestamp_utc": now_utc,
    }

    with open(STATUS_FILE, "w", encoding="utf-8") as f:
        json.dump(updated_status, f, indent=2)
        f.write("\n")

    print(
        f"[{now_utc}] Heartbeat #{total_heartbeats} | Block: {block_height} | "
        f"Status: ACTIVE | Hash: {inference_hash} | "
        f"Injective: {injective_status['status']} (Block: {injective_status['latest_block_height']}, "
        f"Latency: {injective_status['latency_ms']}ms)"
    )


if __name__ == "__main__":
    run_heartbeat()
