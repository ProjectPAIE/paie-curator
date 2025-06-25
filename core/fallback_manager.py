# core/fallback_manager.py (V1.1 - With Redis Escalation)
import json
import redis
from datetime import datetime
from pathlib import Path
from typing import Literal

from .logger_setup import logger
from .config_loader import DB_CONFIG # Re-using DB_CONFIG for Redis host for simplicity

FAIL_LOG_PATH = Path(__file__).parent.parent / "fail_log.jsonl"
REDIS_QUEUE_NAME = "think_tank_escalation_queue"

FailureReason = Literal[
    "INTENT_UNKNOWN", 
    "SCHEMA_SELECTION_FAILED", 
    "PARSING_ERROR"
]

def handle_fallback(
    reason: FailureReason, 
    user_input: str, 
    module_origin: str, 
    llm_output: str = "N/A"
):
    """
    The main entry point for any failure. It logs the failure locally
    and pushes an escalation packet to the Redis queue for future processing.
    """
    # 1. Create the structured failure packet
    fallback_payload = {
        "timestamp": datetime.now().isoformat(),
        "input_text": user_input,
        "failure_reason": reason,
        "module_origin": module_origin,
        "llm_guess": llm_output
    }
    
    # 2. Log the failure locally to fail_log.jsonl
    try:
        logger.warning(f"Logging failure from '{module_origin}': {reason}")
        with open(FAIL_LOG_PATH, 'a') as f:
            f.write(json.dumps(fallback_payload) + '\n')
    except Exception as e:
        logger.error(f"CRITICAL: Could not write to fail_log.jsonl. Error: {e}", exc_info=True)

    # 3. Push the escalation packet to the Redis queue
    try:
        # NOTE: We are re-using the DB_CONFIG host/port for Redis as they run on the same server.
        r = redis.Redis(host=DB_CONFIG.get('host'), port=DB_CONFIG.get('port', 6379), db=0)
        r.rpush(REDIS_QUEUE_NAME, json.dumps(fallback_payload))
        logger.info(f"Successfully pushed escalation packet for '{reason}' to Redis queue.")
    except Exception as e:
        logger.error(f"CRITICAL: Could not push escalation packet to Redis. Is Redis running? Error: {e}", exc_info=True)
