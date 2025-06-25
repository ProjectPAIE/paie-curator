# PAIE Curator

**A Local LLM Listener That Learns With You**

---

## 🚀 What This Is

This is the first operational node in a Mesh.  
A listener. A watcher. A curator of intelligence.

It connects to a Redis queue and listens for escalated LLM failures — things your models *couldn’t classify*, or *got wrong*, or *needed help thinking about again*. It’s schema-aware. Human-aligned. And model-agnostic.

You don’t need our front-end. You don’t need a massive model.  
All you need is **a model that knows when it’s unsure**, and this listener will do the rest.

---

## 🧠 Why We Built This

Most current "MCP" systems focus on RAG, vector search, or agent orchestration.  
We chose something simpler. **Structured escalation** — one of the most overlooked tools in LLM engineering.

If you want smarter models, you don’t need bigger ones.  
You need better memory.  
You need **a place for the misses to go**.  
That’s what this is.

We built it because we were tired of everyone skipping the hard part: _structured thought_.

---

## 📦 What’s Inside

- `core/`: Schema router, fallback handler, structured ingest logic
- `mcp/`: Real-time Redis listener (`mcp_listener.py`)
- `main.py`: Entry point if you want CLI testing
- `check_escalations.py`: View what your models escalated
- `fail_log.jsonl`: Output of escalated records

---

## 🛠 How to Use

1. Start a Redis server locally (default: `localhost:6379`)
2. Run the listener:

   ```bash
   ./start_listener.sh
