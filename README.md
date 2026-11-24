# decentralized-ai-inference-node
24/7 Autonomous AI Inference &amp; Light Validator Node with automated GitHub Actions heartbeat ⚡🌐
# decentralized-ai-inference-node

24/7 Autonomous AI Inference & Light Validator Node with automated GitHub Actions heartbeat ⚡🌐

## Architecture

This repository runs a lightweight, serverless AI inference & validator heartbeat node powered by GitHub Actions:

```
+-----------------------------------+
|   GitHub Actions Cron Scheduler   |
|     (Every 6 Hours: 0 */6 * * *)  |
+-----------------+-----------------+
                  |
                  v
+-----------------------------------+
|         node_runner.py            |
|  - Increments Block Height        |
|  - Generates Inference Hash       |
|  - Logs UTC Heartbeat Timestamp   |
+-----------------+-----------------+
                  |
                  v
+-----------------------------------+
|           status.json             |
|  Auto-committed to main branch    |
+-----------------------------------+
```

## Features

- **Autonomous 24/7 Operation**: Runs on GitHub cloud runners every 6 hours (`0 */6 * * *`) without local hardware.
- **Manual Trigger Support**: Supports on-demand execution via `workflow_dispatch` in the Actions tab.
- **Lightweight Python Runner**: Zero external dependencies; uses Python standard library (`json`, `os`, `datetime`, `hashlib`).
- **Verifiable State Tracking**: Persists node status, block height, AI inference heartbeat, and UTC timestamp in `status.json`.
- **Automated State Commits**: Automatically commits updated `status.json` back to the `main` branch.

## Setup Guide

1. **Clone the repository**
   ```bash
   git clone https://github.com/Darkshanu/decentralized-ai-inference-node.git
   cd decentralized-ai-inference-node
   ```

2. **Run locally (optional)**
   ```bash
   python node_runner.py
   ```
   This creates or updates `status.json` with the latest block height, inference hash, and timestamp.

3. **Enable GitHub Actions**
   - Ensure GitHub Actions are enabled in your repository **Settings -> Actions -> General**.
   - Workflow permissions must allow read and write (`permissions: contents: write` is already configured in `.github/workflows/node-heartbeat.yml`).

4. **Manual Trigger**
   - Go to the **Actions** tab, select **Node Heartbeat**, and click **Run workflow**.
