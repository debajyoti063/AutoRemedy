import redis
import json
import hashlib

r = redis.Redis()

def event_hash(event):
    # Use relevant fields for hash (customize as needed)
    key = f"{event.get('event_type')}|{event.get('details', {}).get('source')}|{event.get('details', {}).get('description')}"
    return hashlib.sha256(key.encode('utf-8')).hexdigest()

def store_feedback(event, action, feedback, comment=None):
    key = f"feedback:event:{event_hash(event)}"
    entry = {"action": action, "feedback": feedback, "comment": comment}
    r.rpush(key, json.dumps(entry))

def get_feedback(event):
    key = f"feedback:event:{event_hash(event)}"
    return [json.loads(x) for x in r.lrange(key, 0, -1)] 