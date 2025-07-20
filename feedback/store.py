import redis
import json
import hashlib
import os
from utils.config_loader import load_config, get_redis_config

config = load_config()
REDIS_HOST, REDIS_PORT, REDIS_DB = get_redis_config(config)
r = redis.Redis(host=REDIS_HOST, port=REDIS_PORT, db=REDIS_DB, decode_responses=True)

def event_hash(event):
    # Use relevant fields for hash (customize as needed)
    details = event.get('details') or {}
    key = f"{event.get('event_type')}|{details.get('source')}|{details.get('description')}"
    return hashlib.sha256(key.encode('utf-8')).hexdigest()

def store_feedback(event, action, feedback, comment=None):
    key = f"feedback:event:{event_hash(event)}"
    entry = {"action": action, "feedback": feedback, "comment": comment}
    r.rpush(key, json.dumps(entry))

def get_feedback(event):
    key = f"feedback:event:{event_hash(event)}"
    return [json.loads(x) for x in r.lrange(key, 0, -1)] 