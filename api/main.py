from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse
from api.models import EventIn, FeedbackIn, StatusOut, HistoryOut, HistoryRecord
import os
import redis
import json
from typing import List
from feedback.store import store_feedback
import logging
from utils.config_loader import load_config, get_redis_config

app = FastAPI(title="AutoRemedy API", description="REST API for the AutoRemedy agentic system.")

# Set up logging
logger = logging.getLogger("api")
handler = logging.FileHandler("logs/api.log", encoding="utf-8")
formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
handler.setFormatter(formatter)
if not logger.hasHandlers():
    logger.addHandler(handler)
logger.setLevel(logging.INFO)

# Redis connection (configurable via env)
config = load_config()
REDIS_HOST, REDIS_PORT, REDIS_DB = get_redis_config(config)
logger.info(f"[DEBUG] API Redis config: REDIS_HOST={REDIS_HOST}, REDIS_PORT={REDIS_PORT}, REDIS_DB={REDIS_DB}")
print(f"[DEBUG] API Redis config: REDIS_HOST={REDIS_HOST}, REDIS_PORT={REDIS_PORT}, REDIS_DB={REDIS_DB}")
redis_client = redis.Redis(host=REDIS_HOST, port=REDIS_PORT, db=REDIS_DB, decode_responses=True)
logger.info(f"[DEBUG] API Redis client connection kwargs: {redis_client.connection_pool.connection_kwargs}")
print(f"[DEBUG] API Redis client connection kwargs: {redis_client.connection_pool.connection_kwargs}")

EVENT_QUEUE = "agentic:events"
HISTORY_LIST = "agentic:history"

@app.get("/")
def root():
    return {"message": "AutoRemedy API is running"}

@app.get("/health", response_model=StatusOut)
def health():
    try:
        redis_client.ping()
        return StatusOut(status="ok")
    except Exception as e:
        return StatusOut(status="error", detail=str(e))

@app.post("/event")
def submit_event(event: EventIn):
    logger.info(f"[DEBUG] Submitting event: {event.dict()} to Redis host={REDIS_HOST}, port={REDIS_PORT}")
    print(f"[DEBUG] Submitting event: {event.dict()} to Redis host={REDIS_HOST}, port={REDIS_PORT}")
    # Push event to Redis queue
    redis_client.rpush(EVENT_QUEUE, event.json())
    return {"status": "submitted"}

@app.get("/history", response_model=HistoryOut)
def get_history():
    # Get all history records from Redis
    records = []
    for item in redis_client.lrange(HISTORY_LIST, 0, -1):
        try:
            record = json.loads(item)
            records.append(record)
        except Exception:
            continue
    return HistoryOut(records=records)

@app.post("/feedback")
def submit_feedback(feedback: FeedbackIn):
    # Find the history record by event_id
    history = redis_client.lrange(HISTORY_LIST, 0, -1)
    found_event = None
    for item in history:
        record = json.loads(item)
        if str(record['event'].get('job_id')) == str(feedback.event_id):
            found_event = record['event']
            break
    if not found_event:
        raise HTTPException(status_code=404, detail="Event not found in history")
    # Store feedback using the new feedback store
    store_feedback(found_event, action="unknown", feedback=feedback.rating, comment=feedback.comment)
    return {"status": "feedback added"}

@app.get("/status", response_model=StatusOut)
def get_status():
    # Simple status endpoint (could be expanded)
    try:
        event_queue_len = redis_client.llen(EVENT_QUEUE)
        history_len = redis_client.llen(HISTORY_LIST)
        return StatusOut(status="ok", detail=f"event_queue={event_queue_len}, history={history_len}")
    except Exception as e:
        return StatusOut(status="error", detail=str(e)) 