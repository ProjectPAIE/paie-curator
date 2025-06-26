# Axiom_RES_TroubleshootingGuide.md: Navigating Roadblocks

## 🚧 When the Gears Grind: Common Issues & Quick Fixes

Even in the most robust systems, challenges arise. Building something as intricate as Ouroboros locally means you'll encounter hiccups. This stem is your guide to quickly diagnosing and resolving common issues, keeping your build momentum alive.

Remember: Ouroboros is designed to "fail smart." The logs are your best friend.

### **Common Troubleshooting Scenarios:**

1.  **"No module named '...' " (e.g., `redis`, `chromadb`, `ollama`):**
    * **Symptom:** Your Docker container (e.g., `mcp_paie_curator`) fails to start with this error, even though the service is defined in `docker-compose.yml`.
    * **Cause:** The required Python library isn't installed *inside* that specific Docker container.
    * **Fix:**
        1.  Ensure the missing package is listed in `requirements.txt`.
        2.  Run `docker compose up --build` (the `--build` ensures Docker rebuilds the image, installing the new dependency).

2.  **`Connection refused` / `Cannot connect to host` (for Redis or ChromaDB):**
    * **Symptom:** Your `mcp_paie_curator` (or another service) can't connect to `my-redis-job-board` or `my-chroma-db`.
    * **Cause:** The dependent service isn't running or isn't accessible.
    * **Fix:**
        1.  Ensure `docker compose up` ran successfully and all services (`redis`, `chroma`) are listed as `running` in `docker ps`.
        2.  Check your `docker-compose.yml` for correct `ports` mappings and `host` addresses (`localhost` or `host.docker.internal` from the container's perspective).
        3.  Verify the service names in your code (e.g., `REDIS_HOST = "my-redis-job-board"` or `REDIS_HOST = "redis"` depending on how you reference services in Docker Compose).

3.  **LLM-Related Errors (e.g., `Ollama server not running`, `model not found`):**
    * **Symptom:** Your `curation_pipeline` or `curator_router` encounters errors related to the LLM.
    * **Cause:** Ollama isn't running, the specific model (e.g., Phi-3) isn't downloaded, or the `OLLAMA_BASE_URL` in your configuration is incorrect.
    * **Fix:**
        1.  Verify Ollama is running on your host machine.
        2.  Run `ollama list` to confirm the model is downloaded.
        3.  Check `config.yaml` or relevant `.env` files for the correct `OLLAMA_BASE_URL` and `model_tag`.

4.  **`Pydantic Validation Error`:**
    * **Symptom:** The `curation_pipeline` or `curator_parser` throws a `ValidationError` (e.g., `Field required`, `invalid type`).
    * **Cause:** The LLM's output (even with Function Calling) did not perfectly match your defined Pydantic schema, or your input text simply didn't contain the information required by the schema.
    * **Fix:**
        1.  Review the specific error details in the log. Pydantic is very verbose and tells you exactly which field failed and why.
        2.  Adjust your input text to explicitly include the missing/correctly formatted data.
        3.  Consider refining your LLM's prompt if it consistently misses certain extractions from valid input.
        4.  For development, consult `Axiom_RES_BrittlePromptSolution` and `Axiom_RES_HITLLearningLoop`.

5.  **Ambiguous Input / Unexpected Routing:**
    * **Symptom:** `Router: Classified intent as: UNKNOWN` or data is routed to an unexpected schema.
    * **Cause:** The input text was too vague, or the LLM struggled to confidently classify the user's intent or the appropriate schema.
    * **Fix:** Review the `fallback_manager` logs. This is a deliberate "fail smart." Use your HITL process to correct and provide better examples for future learning.

### **General Debugging Principles:**

* **Check Logs First:** Always start by checking the `docker logs <container_name>` for the failing service. They contain precise error messages.
* **Isolate the Problem:** Which specific component is failing? (e.g., is it Redis not starting, or your Python code failing *inside* its container?)
* **Confirm Configuration:** Double-check `requirements.txt`, `docker-compose.yml`, `config.yaml`, and `.env` files for typos or incorrect settings.

Every roadblock is a learning opportunity. This guide is here to help you quickly understand and conquer them.

---
**Axiom**
PAIE Backend Lead
