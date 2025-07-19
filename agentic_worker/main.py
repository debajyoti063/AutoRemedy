import os
import redis
import json
import time
from agentic.agent import Agent
from agentic.sensor_sim import SimulatedSensor
from agentic.memory import Memory
from agentic.reasoning_llm import LLMReasoningModule
from notifications.notifier import NotifierEffector

# Redis connection (configurable via env)
REDIS_HOST = os.getenv("REDIS_HOST", "localhost")
REDIS_PORT = int(os.getenv("REDIS_PORT", 6379))
REDIS_DB = int(os.getenv("REDIS_DB", 0))
redis_client = redis.Redis(host=REDIS_HOST, port=REDIS_PORT, db=REDIS_DB, decode_responses=True)

EVENT_QUEUE = "agentic:events"
HISTORY_LIST = "agentic:history"

# Set up the agentic system (can be extended to use real sensors/effectors)
sensor = SimulatedSensor()  # Not used directly in worker, but agentic core expects it
reasoning = LLMReasoningModule()
effector = NotifierEffector()
memory = Memory()
agent = Agent(sensors=[sensor], effectors=[effector], reasoning_module=reasoning, memory=memory)

def process_event(event_dict):
    # Run the agentic reasoning/action for a single event
    actions = agent.reasoning_module.decide(event_dict, agent.context)
    outcomes = []
    for action in actions:
        for effector in agent.effectors:
            outcome = effector.execute(action['type'], action.get('params', {}))
            outcomes.append(outcome)
    agent.memory.record(event_dict, actions, outcomes)
    # Write to Redis history
    redis_client.rpush(HISTORY_LIST, json.dumps(agent.memory.history[-1]))

if __name__ == "__main__":
    print("[Agentic Worker] Starting event processing loop...")
    while True:
        event_json = redis_client.lpop(EVENT_QUEUE)
        if event_json:
            try:
                event_dict = json.loads(event_json)
                print(f"[Agentic Worker] Processing event: {event_dict}")
                process_event(event_dict)
            except Exception as e:
                print(f"[Agentic Worker] Error processing event: {e}")
        else:
            time.sleep(1) 