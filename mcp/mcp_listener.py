# mcp/mcp_listener.py
# Version 0.1 - MCP Mesh Daemon (First Breath)

import redis
import json
import time
from datetime import datetime

QUEUE_NAME = "think_tank_escalation_queue"
REDIS_HOST = "localhost"
REDIS_PORT = 6379

print("[MCP LISTENER] Booting up...")

def process_escalation(packet):
    print("\n--- [MCP Listener] Escalation Detected ---")
    for k, v in packet.items():
        print(f"{k}: {v}")
    print("[MCP Listener] Escalation processed. (No action taken yet)")


def main():
    r = redis.Redis(host=REDIS_HOST, port=REDIS_PORT, db=0)
    print("[MCP Listener] Connected to Redis. Listening...")

    while True:
        item = r.rpop(QUEUE_NAME)
        if item:
            try:
                data = json.loads(item.decode("utf-8"))
                process_escalation(data)
            except Exception as e:
                print(f"[MCP Listener] Error decoding packet: {e}")
        else:
            time.sleep(1)  # Poll every second


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n[MCP Listener] Shutting down.")

