import yaml
from jobsim.simulator import create_jobs_from_config
from llm.llama3_client import Llama3Client
from agent.orchestrator import JobAgent
from rich.console import Console
from utils.config_loader import load_config, get_llm_config

console = Console()

def main():
    console.print("[bold blue]\n=== AutoRemedy Job Monitoring POC ===\n[/bold blue]")
    config = load_config()
    jobs = create_jobs_from_config(config['jobs'])
    # Use LLM config with env var fallback
    llm_client = Llama3Client(config)
    agent = JobAgent(jobs, config, llm_client)
    agent.monitor()
    console.print("[bold green]\nPOC run complete. Check above for job results and escalations.\n[/bold green]")

if __name__ == "__main__":
    main() 