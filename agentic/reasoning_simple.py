from agentic.base import ReasoningModule
from typing import Dict, Any, List

class SimpleReasoningModule(ReasoningModule):
    def decide(self, event: Dict[str, Any], context: Dict[str, Any]) -> List[Dict[str, Any]]:
        actions = []
        if event['status'] in ['fail', 'stuck']:
            actions.append({
                'type': 'notify',
                'params': {
                    'job': event,  # Use the event dict directly
                    'escalation': True
                }
            })
        else:
            actions.append({
                'type': 'notify',
                'params': {
                    'job': event,
                    'escalation': False
                }
            })
        return actions 