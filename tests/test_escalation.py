import requests
import time
import os

event = {
    "job_id": 999,
    "status": "escalate",
    "event_type": "job_issue",
    "details": {
        "timestamp": "2024-07-19T12:00:00Z",
        "source": "CriticalService",
        "description": "Fatal error: system overheating. Immediate escalation required."
    },
    "escalate": True
}

# Post the event to the API
r = requests.post("http://localhost:8000/event", json=event)
print("Event submission status:", r.status_code)

# Wait for the worker to process
print("Waiting for worker to process event...")
time.sleep(2)

# Check escalation log
log_path = os.path.join("logs", "escalation.log")
if os.path.exists(log_path):
    with open(log_path, encoding="utf-8") as f:
        log_content = f.read()
        print("Escalation log content:\n", log_content[-1000:])
else:
    print("Escalation log not found.") 