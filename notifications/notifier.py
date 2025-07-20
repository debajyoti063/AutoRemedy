from rich.console import Console
from agentic.base import Effector
from typing import Any, Dict
import logging
import os

console = Console()

# Ensure logs directory exists
os.makedirs('logs', exist_ok=True)
escalation_logger = logging.getLogger('escalation')
if not escalation_logger.hasHandlers():
    fh = logging.FileHandler('logs/escalation.log', encoding="utf-8")
    formatter = logging.Formatter('%(asctime)s %(message)s')
    fh.setFormatter(formatter)
    escalation_logger.addHandler(fh)
    escalation_logger.setLevel(logging.INFO)

class NotifierEffector(Effector):
    def execute(self, action: str, params: Dict[str, Any]) -> Any:
        job = params.get('job')
        escalation = params.get('escalation', False)
        remediation = params.get('remediation')
        if action == 'notify':
            if escalation:
                console.print(f"[bold red]ESCALATION: Manual intervention required for job {job['job_id']}![/bold red]")
                print(f"[DEBUG] Escalation logging triggered for job {job['job_id']}")
                escalation_logger.info(f"ESCALATED EVENT: {job}")
                print(f"*** ESCALATION TRIGGERED ***: {job}")
            else:
                console.print(f"[yellow]Notification: Issue detected and handled for job {job['job_id']} (status: {job['status']})[/yellow]")
        elif action == 'remediate':
            console.print(f"[green]Remediation action: {remediation} for job {job['job_id']} (status: {job['status']})[/green]")
            print(f"[DEBUG] Remediation action triggered: {remediation} for job {job['job_id']}")
        else:
            console.print(f"[red]Unknown action: {action}[/red]")

def notify(job, config, escalation=False):
    eff = NotifierEffector()
    # Support both dict and SimulatedJob
    if hasattr(job, 'job_id') and hasattr(job, 'status'):
        job_dict = {'job_id': job.job_id, 'status': job.status}
    else:
        job_dict = job
    eff.execute('notify', {'job': job_dict, 'escalation': escalation}) 