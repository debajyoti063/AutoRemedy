import uvicorn
from fastapi import FastAPI, Request
from pydantic import BaseModel
from typing import Any, Dict
import json
import yaml
import os
import sys
sys.path.append(os.path.abspath(".."))  # Ensure project root is in path

from llm.llama3_client import Llama3Client
from resolution.engine import handle_issue
from notifications.notifier import NotifierEffector
from utils.config_loader import load_config

app = FastAPI(title="AutoRemedy MCP Server")

# Load tool schemas from YAML config
def load_tool_registry(path="mcp_server/tool_schemas.yaml"):
    if os.path.exists(path):
        with open(path, "r", encoding="utf-8") as f:
            return yaml.safe_load(f)
    return {}

TOOL_REGISTRY = load_tool_registry()

# Load config for LLM and remediation
CONFIG = load_config()
llm_client = Llama3Client(CONFIG)
notifier = NotifierEffector()

def remediate_issue(job_id: str, status: str, details: dict = None) -> Dict[str, Any]:
    event = {"job_id": job_id, "status": status, "details": details or {}, "event_type": "job_issue"}
    # Use remediation rules from config
    actions = CONFIG.get("resolution", {}).get(status, [])
    results = []
    for action in actions:
        result = handle_issue(event, action, llm_client)
        results.append({"action": action, "result": result})
    return {"result": results, "success": any(r["result"] != "escalate" for r in results)}

def escalate_issue(job_id: str, reason: str) -> Dict[str, Any]:
    event = {"job_id": job_id, "status": "escalate", "details": {"reason": reason}, "event_type": "job_issue", "escalate": True}
    notifier.execute("notify", {"job": event, "escalation": True})
    return {"escalated": True, "message": f"Job {job_id} escalated: {reason}"}

def analyze_log(log_text: str, job_id: str) -> Dict[str, Any]:
    suggestion = llm_client.analyze_log(log_text, job_id=job_id)
    return {"suggestion": suggestion}

TOOL_IMPLS = {
    "remediate_issue": remediate_issue,
    "escalate_issue": escalate_issue,
    "analyze_log": analyze_log
}

@app.post("/mcp")
async def mcp_endpoint(request: Request):
    data = await request.json()
    method = data.get("method")
    params = data.get("params", {})
    if method in TOOL_IMPLS:
        result = TOOL_IMPLS[method](**params)
        return {"jsonrpc": "2.0", "result": result, "id": data.get("id")}
    return {"jsonrpc": "2.0", "error": {"code": -32601, "message": "Method not found"}, "id": data.get("id")}

@app.get("/mcp/tools")
def list_tools():
    return {"tools": [{"name": k, **v} for k, v in TOOL_REGISTRY.items()]}

if __name__ == "__main__":
    uvicorn.run("mcp_server.mcp_adapter:app", host="0.0.0.0", port=9000, reload=True) 