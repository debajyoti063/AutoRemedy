import redis
import json
import time

# Test events matching remediation.yaml rules
TEST_EVENTS = [
    {
        'job_id': 2001,
        'status': 'fail',
        'event_type': 'job_issue',
        'details': {
            'timestamp': '2024-07-19T12:00:00Z',
            'source': 'TestSource',
            'description': 'Service crashed unexpectedly.'
        }
    },
    {
        'job_id': 2002,
        'status': 'fail',
        'event_type': 'job_issue',
        'details': {
            'timestamp': '2024-07-19T12:01:00Z',
            'source': 'DiskMonitor',
            'description': 'Disk full on /dev/sda1.'
        }
    },
    {
        'job_id': 2003,
        'status': 'fail',
        'event_type': 'job_issue',
        'details': {
            'timestamp': '2024-07-19T12:02:00Z',
            'source': 'Updater',
            'description': 'update failed due to network error.'
        }
    },
    {
        'job_id': 2004,
        'status': 'fail',
        'event_type': 'job_issue',
        'details': {
            'timestamp': '2024-07-19T12:03:00Z',
            'source': 'UnknownSource',
            'description': 'No remediation rule should match.'
        }
    }
]

def test_remediation_config():
    r = redis.Redis()
    for event in TEST_EVENTS:
        r.lpush('agentic:events', json.dumps(event))
    print("[TEST] Pushed remediation test events to queue.\nPlease observe the worker output for remediation actions.")
    # Wait for worker to process events
    time.sleep(5)
    # This test is observational: check the worker console/logs for remediation actions.
    # For full automation, you could parse logs or extend the effector to record actions to a file/db for assertion.

if __name__ == "__main__":
    test_remediation_config() 