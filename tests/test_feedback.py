import pytest
from feedback.store import store_feedback, get_feedback, event_hash, r
from feedback.adapter import enrich_prompt_with_feedback

# Dummy event for testing
DUMMY_EVENT = {
    "job_id": 123,
    "status": "fail",
    "event_type": "job_issue",
    "details": {
        "timestamp": "2024-07-19T12:00:00Z",
        "source": "TestSource",
        "description": "Disk full error"
    }
}

def test_feedback_submission_and_retrieval():
    store_feedback(DUMMY_EVENT, "clear_temp_files", "ineffective", "Disk still full")
    feedbacks = get_feedback(DUMMY_EVENT)
    assert feedbacks[-1]["feedback"] == "ineffective"
    assert feedbacks[-1]["action"] == "clear_temp_files"
    assert feedbacks[-1]["comment"] == "Disk still full"

def test_prompt_enrichment():
    prompt = "Analyze this log."
    feedbacks = [{"action": "clear_temp_files", "feedback": "ineffective", "comment": "Disk still full"}]
    enriched = enrich_prompt_with_feedback(prompt, feedbacks)
    assert "Feedback history" in enriched and "Disk still full" in enriched

def test_no_feedback():
    # Use a unique event hash to ensure no feedback
    event = dict(DUMMY_EVENT)
    event["job_id"] = 99999
    # Clear feedback for this event hash
    r.delete(f"feedback:event:{event_hash(event)}")
    feedbacks = get_feedback(event)
    assert feedbacks == []
    prompt = "Analyze this log."
    enriched = enrich_prompt_with_feedback(prompt, feedbacks)
    assert enriched == prompt 