import time
from .actions import ACTION_REGISTRY

def handle_issue(job, action, llm_client):
    action_func = ACTION_REGISTRY.get(action)
    if action_func:
        return action_func(job, llm_client)
    else:
        print(f"[Resolution] Unknown action '{action}' for job {job.job_id}.")
        return "unknown" 