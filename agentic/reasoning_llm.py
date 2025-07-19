from agentic.base import ReasoningModule
from typing import Dict, Any, List
from llm.llama3_client import Llama3Client
import yaml
from feedback.store import get_feedback
from feedback.adapter import enrich_prompt_with_feedback
from remediation.engine import load_remediation_rules, find_remediation_action

class LLMReasoningModule(ReasoningModule):
    def __init__(self, config_path='config.yaml'):
        with open(config_path, 'r') as f:
            config = yaml.safe_load(f)
        self.llm_client = Llama3Client(config)
        self.remediation_rules = load_remediation_rules()

    def decide(self, event: Dict[str, Any], context: Dict[str, Any]) -> List[Dict[str, Any]]:
        # Compose a detailed log or event description for the LLM
        details = event.get('details', {})
        log_text = (
            f"Job ID: {event.get('job_id')}\n"
            f"Status: {event.get('status')}\n"
            f"Event Type: {event.get('event_type')}\n"
            f"Timestamp: {details.get('timestamp')}\n"
            f"Source: {details.get('source')}\n"
            f"Description: {details.get('description')}"
        )
        # Retrieve feedback for similar events
        feedback_list = get_feedback(event)
        # Enrich prompt with feedback
        prompt = enrich_prompt_with_feedback(f"{self.llm_client.prompt_template}\n{log_text}", feedback_list)
        # Call LLM for suggestion
        suggestion = self.llm_client.analyze_log(prompt, job_id=event.get('job_id'))
        actions = []
        # Escalation logic: escalate if LLM says so, or if event has escalate True or status 'escalate'
        escalate = (
            'escalate' in suggestion.lower() or
            event.get('escalate') is True or
            str(event.get('status', '')).lower() == 'escalate'
        )
        if escalate:
            actions.append({
                'type': 'notify',
                'params': {
                    'job': event,
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
        # Configurable remediation logic
        remediation_action = find_remediation_action(event, self.remediation_rules)
        if remediation_action:
            actions.append({
                'type': 'remediate',
                'params': {
                    'job': event,
                    'remediation': remediation_action
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