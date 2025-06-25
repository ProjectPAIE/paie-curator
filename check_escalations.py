import redis
import json

r = redis.Redis(host="localhost", port=6379, db=0)
queue_name = "think_tank_escalation_queue"

items = r.lrange(queue_name, 0, -1)
print(f"\nTotal items in queue: {len(items)}\n")

for i, item in enumerate(items, 1):
    try:
        data = json.loads(item.decode("utf-8"))
        print(f"--- Escalation Packet {i} ---")
        for k, v in data.items():
            print(f"{k}: {v}")
        print()
    except Exception as e:
        print(f"Error decoding item {i}: {e}")
