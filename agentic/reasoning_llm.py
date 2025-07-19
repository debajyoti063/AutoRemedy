from agentic.base import ReasoningModule
from typing import Dict, Any, List
from llm.llama3_client import Llama3Client
import yaml

class LLMReasoningModule(ReasoningModule):
    def __init__(self, config_path='config.yaml'):
        with open(config_path, 'r') as f:
            config = yaml.safe_load(f)
        self.llm_client = Llama3Client(config)

    def decide(self, event: Dict[str, Any], context: Dict[str, Any]) -> List[Dict[str, Any]]:
        # Compose a log or event description for the LLM
        log_text = f"Job {event['job_id']} encountered status: {event['status']}"
        # Call LLM for suggestion
        suggestion = self.llm_client.analyze_log(log_text, job_id=event['job_id'])
        # Parse LLM response into actions (simple keyword-based for demo)
        actions = []
        if 'escalate' in suggestion.lower():
            actions.append({
                'type': 'notify',
                'params': {
                    'job': event,  # Use the event dict directly
                    'escalation': True
                }
            })
        elif 'notify' in suggestion.lower():
            actions.append({
                'type': 'notify',
                'params': {
                    'job': event,
                    'escalation': False
                }
            })
        # Default fallback
        if not actions:
            actions.append({
                'type': 'notify',
                'params': {
                    'job': event,
                    'escalation': False
                }
            })
        return actions 