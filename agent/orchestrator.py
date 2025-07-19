import time
from rich.console import Console
from resolution.engine import handle_issue
from notifications.notifier import notify

console = Console()

class JobAgent:
    def __init__(self, jobs, config, llm_client):
        self.jobs = jobs
        self.config = config
        self.llm_client = llm_client
        self.poll_interval = config.get('poll_interval', 2)
        self.escalation_threshold = config['notifications'].get('escalation_threshold', 2)

    def monitor(self):
        console.print("[bold green]Starting job monitoring...[/bold green]")
        while True:
            for job in self.jobs:
                if job.status == "pending":
                    status = job.run()
                    console.print(f"[cyan]Job {job.job_id} completed with status: {status}[/cyan]")
                    if status in self.config['resolution']:
                        self.handle_issue(job)
            if all(job.status != "pending" for job in self.jobs):
                break
            time.sleep(self.poll_interval)
        console.print("[bold green]All jobs processed.[/bold green]")

    def handle_issue(self, job):
        actions = self.config['resolution'].get(job.status, [])
        for action in actions:
            result = handle_issue(job, action, self.llm_client)
            if result == "escalate":
                notify(job, self.config, escalation=True)
            else:
                notify(job, self.config, escalation=False) 