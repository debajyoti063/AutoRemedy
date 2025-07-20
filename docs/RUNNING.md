# AutoRemedy: Running Locally and in Docker (Config-Driven)

---

## 1. Prerequisites

- Python 3.10+ (for local/script mode)
- Docker & Docker Compose (for containerized mode)
- Redis (runs as a container in Docker mode, or install locally for script mode)
- LM Studio or OpenAI-compatible LLM (for LLM features; can run on host)

---

## 2. Configuration Principles

- All endpoints (Redis, LLM, etc.) are settable via environment variables or `config.yaml`.
- You can override the config file by setting the `CONFIG_FILE` environment variable.
- No code changes are needed to switch between local and Docker.

---

## 3. Running in Docker (Recommended for Production/Testing)

### A. Build and Start All Services

```bash
docker compose up --build
```

- This will start:
  - `api` (FastAPI REST API, port 8000)
  - `worker` (agentic event processor)
  - `redis` (message broker, port 6379)

### B. LLM Server

- Start LM Studio (or your LLM) on your host at port 1234.
- Docker containers will connect to it via `host.docker.internal:1234`.

### C. Environment Variables

- Set in `docker-compose.yml`:
  - `REDIS_HOST=redis`
  - `REDIS_PORT=6379`
  - `LLM_ENDPOINT=http://host.docker.internal:1234/v1`
  - `CONFIG_FILE=config.yaml` (optional, for custom config)

### D. Posting Events

- Use the provided test script:
  ```bash
  python tests/post_kaggle_events.py
  ```
- Or use `curl`:
  ```bash
  curl -X POST http://localhost:8000/event -H "Content-Type: application/json" -d '{"job_id": 123, ...}'
  ```

### E. Checking Logs

- Worker logs: `docker exec autoremedy-worker-1 tail -n 50 /app/logs/worker.log`
- LLM logs: `docker exec autoremedy-worker-1 tail -n 50 /app/logs/llm_analysis.log`
- API logs: `docker exec autoremedy-api-1 tail -n 50 logs/api.log`

---

## 4. Running Locally (Script/Legacy Mode)

### A. Start Redis Locally

- If not already running:
  ```bash
  docker run -p 6379:6379 redis:6
  ```
  or install Redis natively.

### B. (Optional) Set Environment Variables

- You can use a `.env` file or export variables in your shell:
  ```bash
  export REDIS_HOST=localhost
  export REDIS_PORT=6379
  export LLM_ENDPOINT=http://localhost:1234/v1
  export CONFIG_FILE=config.yaml  # or your custom config
  ```

### C. Run the Main Script

- For the legacy agentic loop:
  ```bash
  python main.py
  ```

### D. Run API and Worker Locally (Microservice Mode, No Docker)

- In separate terminals:
  ```bash
  uvicorn api.main:app --reload --port 8000
  python -m agentic_worker.main
  ```

### E. LLM Server

- Start LM Studio (or your LLM) on your host at port 1234.
- The app will connect to `http://localhost:1234/v1` by default.

### F. Posting Events

- Use the test script:
  ```bash
  python tests/post_kaggle_events.py
  ```
- Or use `curl` as above.

---

## 5. Customizing Configuration

- **To use a different config file:**
  ```bash
  export CONFIG_FILE=config.local.yaml
  python main.py
  ```
  or set in Docker Compose:
  ```yaml
  environment:
    - CONFIG_FILE=config.docker.yaml
  ```

- **To override Redis/LLM endpoints:**
  ```bash
  export REDIS_HOST=customhost
  export LLM_ENDPOINT=http://localhost:8080/v1
  ```

---

## 6. Troubleshooting

- **Check logs** in the `logs/` directory or via Docker exec.
- **422 errors** when posting events usually mean the event JSON does not match the expected schema.
- **LLM timeouts** mean the LLM server is not running or not reachable at the configured endpoint.

---

## 7. MCP Server (Optional, for Tool/LLM Interop)

- Start with:
  ```bash
  uvicorn mcp_server.mcp_adapter:app --reload --port 9000
  ```
- Call tools via HTTP POST to `http://localhost:9000/mcp` with JSON-RPC payloads.

---

## 8. Summary Table

| Mode         | Redis Host      | LLM Endpoint                        | How to Run                        |
|--------------|----------------|-------------------------------------|-----------------------------------|
| Docker       | redis          | http://host.docker.internal:1234/v1 | `docker compose up --build`       |
| Local Script | localhost      | http://localhost:1234/v1            | `python main.py`                  |
| Local Micro  | localhost      | http://localhost:1234/v1            | `uvicorn api.main:app ...` + `python -m agentic_worker.main` |

---

**You can now run AutoRemedy anywhere, with no code changes—just set the right config or environment variables!** 