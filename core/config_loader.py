# core/config_loader.py (V1.3 - Final Docker-Aware)
import yaml
from pathlib import Path
import os

CONFIG_FILE_PATH = Path(__file__).parent.parent / "config.yaml"

def load_config() -> dict:
    try:
        with open(CONFIG_FILE_PATH, "r") as f:
            config = yaml.safe_load(f)
        return config if config else {}
    except Exception as e:
        print(f"FATAL ERROR: Could not load configuration. Error: {e}")
        return {}

config = load_config()

DB_CONFIG = config.get("database", {})
MODEL_CONFIG = config.get("models", {})

# Use Docker-internal hostname (default: 'ollama') for LLM connection
OLLAMA_HOST = MODEL_CONFIG.get('ollama_host', 'localhost')
OLLAMA_BASE_URL = f"http://{OLLAMA_HOST}:11434"
