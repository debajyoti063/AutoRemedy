from typing import List, Dict, Any
from agentic.base import Sensor, Effector, ReasoningModule
from agentic.memory import Memory

class Agent:
    def __init__(self, sensors: List[Sensor], effectors: List[Effector], reasoning_module: ReasoningModule, memory: Memory = None):
        self.sensors = sensors
        self.effectors = effectors
        self.reasoning_module = reasoning_module
        self.memory = memory or Memory()
        self.context = {}  # Can be expanded to persistent memory

    def run_once(self):
        # Collect events from all sensors
        for sensor in self.sensors:
            event = sensor.get_event()
            if event:
                # Decide on actions
                actions = self.reasoning_module.decide(event, self.context)
                outcomes = []
                # Execute actions
                for action in actions:
                    for effector in self.effectors:
                        outcome = effector.execute(action['type'], action.get('params', {}))
                        outcomes.append(outcome)
                # Record in memory
                self.memory.record(event, actions, outcomes)

    def run_forever(self, poll_interval: float = 5.0):
        import time
        while True:
            self.run_once()
            time.sleep(poll_interval)

    def feedback(self, feedback_data: Dict[str, Any]):
        # Store feedback and optionally adapt reasoning or actions
        self.memory.history[-1]['feedback'] = feedback_data
        # Here you could add logic to adapt rules, prompts, etc. based on feedback 