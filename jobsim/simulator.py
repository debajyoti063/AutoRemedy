import random
import time

class SimulatedJob:
    def __init__(self, job_id, expected_duration, job_type):
        self.job_id = job_id
        self.expected_duration = expected_duration
        self.job_type = job_type
        self.status = "pending"
        self.retries = 0
        self.start_time = None
        self.end_time = None
        self.log = ""

    def run(self):
        self.start_time = time.time()
        # Randomly determine outcome
        outcome = random.choices(
            ["success", "failed", "stuck", "slow"],
            weights=[0.7, 0.15, 0.1, 0.05],
            k=1
        )[0]
        self.status = outcome
        duration = self.expected_duration
        if outcome == "slow":
            duration *= random.uniform(1.5, 2.5)
        elif outcome == "stuck":
            duration *= random.uniform(2.5, 5.0)
        time.sleep(duration / 10)  # Simulate time passing (scaled down)
        self.end_time = time.time()
        self.log = f"Job {self.job_id} finished with status: {self.status}"
        return self.status

def create_jobs_from_config(config_jobs):
    jobs = []
    for job_cfg in config_jobs:
        job = SimulatedJob(
            job_id=job_cfg['id'],
            expected_duration=job_cfg['expected_duration'],
            job_type=job_cfg['type']
        )
        jobs.append(job)
    return jobs 