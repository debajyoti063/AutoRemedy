## Running Locally

1. (Optional) Create a `.env` file or export environment variables:
   - `REDIS_HOST=localhost`
   - `REDIS_PORT=6379`
   - `LLM_ENDPOINT=http://localhost:1234/v1`
   - `CONFIG_FILE=config.yaml` (or your custom config)
2. Start Redis locally (or use Docker):
   ```bash
   docker run -p 6379:6379 redis:6
   ```
3. Run the main script:
   ```bash
   python main.py
   ```
4. Run the API and worker (in separate terminals):
   ```bash
   uvicorn api.main:app --reload --port 8000
   python -m agentic_worker.main
   ```

## Running with Docker Compose

1. Build and start all services:
   ```bash
   docker compose up --build
   ```
2. The API will be available at `http://localhost:8000`.
3. LM Studio (or your LLM) should be running on your host at port 1234.
4. Environment variables for Redis and LLM are set in `docker-compose.yml`.

## Configuration

- All config is loaded from `config.yaml` by default.
- You can override with a custom config file by setting `CONFIG_FILE` env var.
- Redis and LLM endpoints can be set via environment variables or in the config file.
- See `utils/config_loader.py` for details.

## Example Local Run Script

```bash
#!/bin/bash
export REDIS_HOST=localhost
export REDIS_PORT=6379
export LLM_ENDPOINT=http://localhost:1234/v1
python main.py
``` 