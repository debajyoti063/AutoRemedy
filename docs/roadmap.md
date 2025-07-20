# AutoRemedy Project Roadmap

## Future Plan & Next Steps (as of 2024-07-19)

### ⚠️ Partially Complete / In Progress
- Docker Compose for API, worker, Redis (ready); K8s/Helm not finalized
- Plug-and-play LLMs/tools (config-driven, extensible, not runtime dynamic)
- Autonomous feedback loop (basic prompt enrichment, not full analytics-driven adaptation)
- MCP cross-agent collaboration (internal only, not tested with external agents)

### ❌ Not Yet Implemented / Next Priorities
- Human-in-the-loop (real-time approval UI/API for remediation/escalation)
- Enhanced memory (vector DB, advanced context retrieval)
- Observability & monitoring (tracing, alerting, dashboards)
- Security & access control (authN/authZ, audit logging)
- Performance optimization (profiling, scaling)
- Full Kubernetes/OpenShift deployment (Helm charts, cloud docs)

---

## Docker-First Workflow (Recommended)

- **How to Run:**
  ```bash
  docker-compose up --build
  ```
- **Services:**
  - `api`: FastAPI REST API (port 8000)
  - `worker`: Agentic worker (processes events, triggers LLM, remediation)
  - `redis`: Message broker/state store (port 6379)
- **LM Studio:**
  - Run separately on host (default port 1234)
  - Ensure LLM client in config points to LM Studio endpoint
- **Testing:**
  - Post events via API or test scripts
  - Check logs/llm_analysis.log for LLM activity
  - Use MCP server as needed (can be added to Compose)

---

## Next Steps
- Finalize Docker Compose for all services (add MCP server if needed)
- Add human-in-the-loop UI/API
- Integrate vector DB for enhanced memory
- Add observability, security, and performance features
- Test MCP endpoints with external agents/tools
- Prepare Helm charts and cloud deployment docs

---

*Last updated: 2024-07-19* 