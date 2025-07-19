from typing import List, Dict, Any

class Memory:
    def __init__(self):
        self.history: List[Dict[str, Any]] = []

    def record(self, event: Dict[str, Any], actions: List[Dict[str, Any]], outcomes: List[Any]):
        self.history.append({
            'event': event,
            'actions': actions,
            'outcomes': outcomes
        })

    def get_history(self) -> List[Dict[str, Any]]:
        return self.history 