import os
import yaml

def load_config():
    config_file = os.getenv("CONFIG_FILE", "config.yaml")
    with open(config_file, "r", encoding="utf-8") as f:
        config = yaml.safe_load(f)
    return config

def get_redis_config(config):
    redis_cfg = config.get("redis", {})
    host = os.getenv("REDIS_HOST", redis_cfg.get("host", "localhost"))
    port = int(os.getenv("REDIS_PORT", redis_cfg.get("port", 6379)))
    db = int(os.getenv("REDIS_DB", redis_cfg.get("db", 0)))
    return host, port, db

def get_llm_config(config):
    llm_cfg = config.get("llm", {})
    endpoint = os.getenv("LLM_ENDPOINT", llm_cfg.get("endpoint", "http://localhost:1234/v1"))
    model = os.getenv("LLM_MODEL", llm_cfg.get("model", "llama-3"))
    prompt = llm_cfg.get("log_analysis_prompt", "Analyze this log and suggest resolution steps:")
    return endpoint, model, prompt 