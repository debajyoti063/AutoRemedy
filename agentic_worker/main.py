import os
import redis
import json
import time
import logging
# DEBUG: Print all environment variables at startup
with open("logs/worker_env.log", "a", encoding="utf-8") as f:
    f.write("ENVIRONMENT VARIABLES AT STARTUP:\n")
    for k, v in os.environ.items():
        f.write(f"{k}={v}\n")
print("[DEBUG] ENVIRONMENT VARIABLES AT STARTUP:")
for k, v in os.environ.items():
    print(f"[DEBUG] {k}={v}")
from agentic.agent import Agent
from agentic.sensor_sim import SimulatedSensor
from agentic.memory import Memory
from agentic.reasoning_llm import LLMReasoningModule
from notifications.notifier import NotifierEffector
from utils.config_loader import load_config, get_redis_config

# Ensure logs directory exists
os.makedirs('logs', exist_ok=True)

# Set up logging
logger = logging.getLogger("agentic_worker")
handler = logging.FileHandler("logs/worker.log", encoding="utf-8")
formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
handler.setFormatter(formatter)
if not logger.hasHandlers():
    logger.addHandler(handler)
logger.setLevel(logging.INFO)

# Redis connection (configurable via env)
config = load_config()
REDIS_HOST, REDIS_PORT, REDIS_DB = get_redis_config(config)
print(f"[DEBUG] REDIS_HOST={REDIS_HOST}, REDIS_PORT={REDIS_PORT}")
with open("logs/worker_env.log", "w", encoding="utf-8") as f:
    f.write(f"REDIS_HOST={REDIS_HOST}\nREDIS_PORT={REDIS_PORT}\n")
redis_client = redis.Redis(host=REDIS_HOST, port=REDIS_PORT, db=REDIS_DB, decode_responses=True)
print(f"[DEBUG] Redis client connection kwargs: {redis_client.connection_pool.connection_kwargs}")
with open("logs/worker_env.log", "a", encoding="utf-8") as f:
    f.write(f"connection_kwargs={redis_client.connection_pool.connection_kwargs}\n")

EVENT_QUEUE = "agentic:events"
HISTORY_LIST = "agentic:history"

# Set up the agentic system (can be extended to use real sensors/effectors)
sensor = SimulatedSensor()  # Not used directly in worker, but agentic core expects it
reasoning = LLMReasoningModule()
effector = NotifierEffector()
memory = Memory()
agent = Agent(sensors=[sensor], effectors=[effector], reasoning_module=reasoning, memory=memory)

def process_event(event_dict):
    logger.info(f"Processing event: {event_dict}")
    # Run the agentic reasoning/action for a single event
    try:
        actions = agent.reasoning_module.decide(event_dict, agent.context)
        outcomes = []
        for action in actions:
            for effector in agent.effectors:
                outcome = effector.execute(action['type'], action.get('params', {}))
                outcomes.append(outcome)
                logger.info(f"Action executed: {action['type']} | Outcome: {outcome}")
        agent.memory.record(event_dict, actions, outcomes)
        # Write to Redis history
        redis_client.rpush(HISTORY_LIST, json.dumps(agent.memory.history[-1]))
        logger.info(f"Event processed and recorded: {event_dict.get('job_id')}")
    except Exception as e:
        logger.error(f"Error in process_event: {e}")
        raise

if __name__ == "__main__":
    print("[Agentic Worker] Starting event processing loop...")
    logger.info("Agentic Worker started event processing loop.")
    while True:
        try:
            event_json = redis_client.lpop(EVENT_QUEUE)
        except Exception as e:
            logger.error(f"Redis connection error: {e}")
            print(f"[Agentic Worker] Redis connection error: {e}")
            time.sleep(2)
            continue
        if event_json:
            try:
                event_dict = json.loads(event_json)
                print(f"[Agentic Worker] Processing event: {event_dict}")
                process_event(event_dict)
            except Exception as e:
                logger.error(f"Error processing event: {e}")
                print(f"[Agentic Worker] Error processing event: {e}")
        else:
            time.sleep(1) 