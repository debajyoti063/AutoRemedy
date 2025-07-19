from agentic.base import Sensor
from typing import Dict, Any
import random

class SimulatedSensor(Sensor):
    def get_event(self) -> Dict[str, Any]:
        # Simulate a random job event
        job_id = random.randint(1, 5)
        status = random.choice(['success', 'fail', 'stuck', 'slow'])
        if status == 'success':
            return None  # No event for successful jobs
        return {
            'job_id': job_id,
            'status': status,
            'event_type': 'job_issue',
        } 