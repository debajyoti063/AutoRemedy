from typing import List, Dict, Any

class SelfReflectionModule:
    def __init__(self, min_failures_for_escalation: int = 3):
        self.min_failures_for_escalation = min_failures_for_escalation

    def reflect(self, memory: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Analyze memory/history and suggest adjustments.
        Returns a dict with suggested context updates (e.g., escalate, change strategy).
        """
        # Count recent failures and ineffective remediations
        recent = memory[-self.min_failures_for_escalation:]
        fail_count = 0
        ineffective_count = 0
        for record in recent:
            event = record.get('event', {})
            if event.get('status') == 'fail':
                fail_count += 1
            feedback = record.get('feedback')
            if feedback and feedback.get('rating', 5) < 3:
                ineffective_count += 1
        suggestions = {}
        if fail_count >= self.min_failures_for_escalation:
            suggestions['escalate'] = True
        if ineffective_count > 0:
            suggestions['review_strategy'] = True
        return suggestions 