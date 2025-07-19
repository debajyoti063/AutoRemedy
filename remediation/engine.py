import yaml
import os

def load_remediation_rules(path=None):
    if path is None:
        path = os.path.join(os.path.dirname(__file__), 'remediation.yaml')
    with open(path, 'r') as f:
        return yaml.safe_load(f)["remediation_rules"]

def find_remediation_action(event, rules):
    for rule in rules:
        match = rule["match"]
        if (
            (match.get("event_type") is None or event.get("event_type") == match["event_type"]) and
            (match.get("status") is None or event.get("status") == match["status"]) and
            (match.get("source") is None or event.get("details", {}).get("source") == match["source"]) and
            (match.get("description_contains") is None or match["description_contains"].lower() in event.get("details", {}).get("description", "").lower())
        ):
            return rule["action"]
    return None 