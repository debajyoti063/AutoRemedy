from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse
from api.models import EventIn, FeedbackIn, StatusOut, HistoryOut, HistoryRecord
import os
import redis
import json
from typing import List

app = FastAPI(title="AutoRemedy API", description="REST API for the AutoRemedy agentic system.")

# Redis connection (configurable via env)
REDIS_HOST = os.getenv("REDIS_HOST", "localhost")
REDIS_PORT = int(os.getenv("REDIS_PORT", 6379))
REDIS_DB = int(os.getenv("REDIS_DB", 0))
redis_client = redis.Redis(host=REDIS_HOST, port=REDIS_PORT, db=REDIS_DB, decode_responses=True)

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
    # Find the history record by event_id and update feedback
    history = redis_client.lrange(HISTORY_LIST, 0, -1)
    updated = False
    for idx, item in enumerate(history):
        record = json.loads(item)
        if str(record['event'].get('job_id')) == str(feedback.event_id):
            record['feedback'] = feedback.dict()
            redis_client.lset(HISTORY_LIST, idx, json.dumps(record))
            updated = True
            break
    if not updated:
        raise HTTPException(status_code=404, detail="Event not found in history")
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