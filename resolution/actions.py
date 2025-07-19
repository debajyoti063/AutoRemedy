import time
import os

def retry(job, llm_client):
    if job.retries < 2:
        job.retries += 1
        job.status = "pending"
        print(f"[Resolution] Retrying job {job.job_id} (attempt {job.retries})...")
        return "retried"
    else:
        print(f"[Resolution] Max retries reached for job {job.job_id}.")
        return "escalate"

def restart_service(job, llm_client):
    print(f"[Resolution] Restarting service for job {job.job_id}...")
    time.sleep(0.5)  # Simulate restart
    job.status = "pending"
    return "restarted"

def escalate(job, llm_client):
    print(f"[Resolution] Escalating job {job.job_id} to manual intervention.")
    if llm_client:
        explanation = llm_client.analyze_log(job.log, job.job_id)
        print(f"[LLM Analysis] {explanation}")
    return "escalate"

def clear_temp_files(job, llm_client):
    print(f"[Resolution] Clearing temp files for job {job.job_id}...")
    # Simulate temp file cleanup
    temp_path = f"/tmp/{job.job_id}_tempfile"
    # In real use, would SSH or use remote API
    print(f"[Resolution] (Simulated) Removed {temp_path}")
    return "cleared_temp_files"

def clear_queue(job, llm_client):
    print(f"[Resolution] Clearing queue for job {job.job_id}...")
    # Simulate queue cleanup
    queue_name = f"queue_{job.job_id}"
    print(f"[Resolution] (Simulated) Cleared {queue_name}")
    return "cleared_queue"

ACTION_REGISTRY = {
    "retry": retry,
    "restart_service": restart_service,
    "escalate": escalate,
    "clear_temp_files": clear_temp_files,
    "clear_queue": clear_queue,
} 