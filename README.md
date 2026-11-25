# decentralized-ai-inference-node

24/7 Autonomous AI Inference & Light Validator Node with automated GitHub Actions heartbeat and live **Injective Mainnet (`injective-1`)** telemetry. ⚡🌐

---

## 🌐 Injective Mainnet (`injective-1`) Live Status Telemetry

Each heartbeat cycle queries the live Injective Mainnet LCD endpoint to verify network connectivity, track the latest on-chain block height, and measure response latency:

| Metric | Value / Description |
| :--- | :--- |
| **Chain ID** | `injective-1` (`injective-mainnet`) |
| **Telemetry Endpoint** | `https://sentry.lcd.injective.network/cosmos/base/tendermint/v1beta1/blocks/latest` |
| **Tracked Fields** | `status`, `latest_block_height`, `latency_ms` |
| **Cadence** | Automated via GitHub Actions (`0 */4 * * *` + manual `workflow_dispatch`) |

---

## 📊 Sample `status.json` Output

The node persists its latest inference and Injective Mainnet telemetry state in [`status.json`](./status.json):

```json
{
  "node_id": "decentralized-ai-node-01",
  "node_status": "ACTIVE",
  "block_height": 1005,
  "total_heartbeats": 5,
  "ai_inference_heartbeat": {
    "status": "HEALTHY",
    "model": "light-validator-v1",
    "inference_hash": "66d08f174f88833e",
    "latency_ms": 42
  },
  "injective_network": {
    "network": "injective-mainnet",
    "endpoint": "https://sentry.lcd.injective.network/cosmos/base/tendermint/v1beta1/blocks/latest",
    "status": "CONNECTED",
    "latest_block_height": 193306270,
    "latency_ms": 771.02
  },
  "timestamp_utc": "2026-11-25T17:59:57Z"
}
```

---

## 🏗️ Architecture

This repository runs a lightweight, serverless AI inference & validator heartbeat node powered by GitHub Actions:

```text
+---------------------------------------+
|     GitHub Actions Cron Scheduler     |
|        (Every 4 Hours: 0 */4 * * *)   |
+---------------------------------------+
                    |
                    v
+---------------------------------------+
|             node_runner.py            |
| - Increments Block Height             |
| - Executes Lightweight AI Inference   |
| - Fetches Injective Mainnet Telemetry |
| - Updates status.json & Timestamps    |
+---------------------------------------+
                    |
                    v
+---------------------------------------+
|        Git Concurrency & Rebase       |
| - Queued Concurrency Group            |
| - git pull --rebase origin main       |
| - Auto-Commits & Pushes status.json   |
+---------------------------------------+
```

---

## ⚙️ Workflow Concurrency & `git pull --rebase` Reliability

To keep automated heartbeat commits conflict-free across scheduled and manual runs, `.github/workflows/node-heartbeat.yml` enforces two reliability safeguards:

1. **Workflow Concurrency Queueing**
   ```yaml
   concurrency:
     group: node-heartbeat-${{ github.ref }}
     cancel-in-progress: false
   ```
   Ensures only one heartbeat job executes at a time per branch while queuing (rather than cancelling) overlapping triggers.

2. **Rebase-Before-Push & Idempotent Commits**
   ```bash
   git diff --staged --quiet || git commit -m "chore: update node heartbeat status"
   git pull --rebase origin main
   git push
   ```
   - `git diff --staged --quiet` prevents empty commits if `status.json` has no changes.
   - `git pull --rebase origin main` replays the local heartbeat commit on top of any newer upstream commits before `git push`, eliminating non-fast-forward push errors.

---

## 🛠️ Tech Stack

- **Runtime**: Python 3.11 (`node_runner.py`)
- **Automation**: GitHub Actions (`node-heartbeat.yml`)
- **Telemetry**: Injective Mainnet (`injective-1`) LCD REST API & JSON state persistence (`status.json`)
