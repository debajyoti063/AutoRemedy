import time
import requests

BASE_URL = "http://localhost:8000"

def test_event_submission():
    payload = {"job_id": 101, "status": "fail", "event_type": "job_issue"}
    r = requests.post(f"{BASE_URL}/event", json=payload)
    assert r.status_code == 200
    assert r.json()["status"] == "submitted"
    print("Event submission: PASSED")

def test_history():
    # Wait and retry for worker to process event
    for _ in range(10):
        r = requests.get(f"{BASE_URL}/history")
        assert r.status_code == 200
        records = r.json().get("records", [])
        if any(rec["event"]["job_id"] == 101 for rec in records):
            print("History retrieval: PASSED")
            return records
        time.sleep(1)
    print("DEBUG: Records returned:", records)
    assert any(rec["event"]["job_id"] == 101 for rec in records), "Event not found in history after retries"

def test_feedback(records):
    # Use the first record's job_id
    job_id = records[0]["event"]["job_id"]
    payload = {"event_id": str(job_id), "user": "tester", "rating": 5, "comment": "Looks good"}
    r = requests.post(f"{BASE_URL}/feedback", json=payload)
    assert r.status_code == 200
    assert r.json()["status"] == "feedback added"
    print("Feedback submission: PASSED")

def test_status():
    r = requests.get(f"{BASE_URL}/status")
    assert r.status_code == 200
    assert r.json()["status"] == "ok"
    print("Status endpoint: PASSED")

def run_all():
    test_event_submission()
    records = test_history()
    test_feedback(records)
    test_status()
    print("All microservice API tests PASSED.")

if __name__ == "__main__":
    run_all() 