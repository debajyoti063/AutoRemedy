from rich.console import Console
from agentic.base import Effector
from typing import Any, Dict

console = Console()

class NotifierEffector(Effector):
    def execute(self, action: str, params: Dict[str, Any]) -> Any:
        job = params.get('job')
        escalation = params.get('escalation', False)
        if action == 'notify':
            if escalation:
                console.print(f"[bold red]ESCALATION: Manual intervention required for job {job['job_id']}![/bold red]")
            else:
                console.print(f"[yellow]Notification: Issue detected and handled for job {job['job_id']} (status: {job['status']})[/yellow]")
        else:
            console.print(f"[red]Unknown action: {action}[/red]") 