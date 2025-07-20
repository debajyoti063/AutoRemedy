from typing import List, Dict, Any
from agentic.base import Sensor, Effector, ReasoningModule
from agentic.memory import Memory

class Agent:
    def __init__(self, sensors: List[Sensor], effectors: List[Effector], reasoning_module: ReasoningModule, memory: Memory = None, self_reflection=None):
        self.sensors = sensors
        self.effectors = effectors
        self.reasoning_module = reasoning_module
        self.memory = memory or Memory()
        self.context = {}  # Can be expanded to persistent memory
        self.self_reflection = self_reflection

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
        # Self-reflection after processing
        if self.self_reflection and self.memory.history:
            suggestions = self.self_reflection.reflect(self.memory.history)
            self.context.update(suggestions)

    def run_forever(self, poll_interval: float = 5.0):
        import time
        while True:
            self.run_once()
            time.sleep(poll_interval)

    def feedback(self, feedback_data: Dict[str, Any]):
        # Store feedback and optionally adapt reasoning or actions
        self.memory.history[-1]['feedback'] = feedback_data
        # Here you could add logic to adapt rules, prompts, etc. based on feedback 

class MultiAgentOrchestrator:
    def __init__(self, agent_configs: list):
        self.agents = []
        for cfg in agent_configs:
            sensors = cfg['sensors']
            effectors = cfg['effectors']
            reasoning_module = cfg['reasoning_module']
            memory = cfg.get('memory')
            agent = Agent(sensors, effectors, reasoning_module, memory)
            self.agents.append(agent)

    def run_once(self):
        for agent in self.agents:
            agent.run_once()

    def run_forever(self, poll_interval: float = 5.0):
        import time
        while True:
            self.run_once()
            time.sleep(poll_interval) 