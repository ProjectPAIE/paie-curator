# Axiom_RES_CorePipelineDeepDive.md: The Core Ingestion Pipeline

## 🧠 Your Data's Journey from Raw to Purposeful

Welcome. You're diving into the heart of Ouroboros's intelligence: the Core Ingestion Pipeline. This is where raw, unstructured text begins its transformation into valuable, schema-compliant, "purposeful data" for your personal knowledge base.

This process is orchestrated within `core/curation_pipeline.py` and relies on a powerful combination of LLMs, Function Calling, and Pydantic validation.

### **The Flow (Simplified):**

1.  **User Input:** (e.g., You paste a note into the UI, or it comes from a future web clipper).
2.  **Intent Routing (`curator_router.py`):** The system first asks an LLM: "What is the user trying to do?" (e.g., `INGEST` new data, `QUERY` existing data). This determines the workflow path.
3.  **Schema Selection (`schema_selector.py`):** If the intent is `INGEST`, another LLM is prompted to identify *which* of your predefined schemas (e.g., `ArtEvent`, `Recipe`, `PersonNote`) best fits the input text. This is crucial for guiding the data's purpose.
4.  **Data Extraction & Pydantic Enforcement (`curator_parser.py`):** This is the **crucial alchemy.**
    * The LLM is given the input text *and* the chosen schema's definition (from your Pydantic model) as a **Function Call**.
    * The LLM *must* then respond by calling that function and populating its arguments with data extracted from the text, precisely matching the schema.
    * **Pydantic** acts as the final gate: it rigorously validates the LLM's output against the schema. If even a tiny detail is off (e.g., missing a required field like 'title' for an ArtEvent), Pydantic catches it immediately.
5.  **Structured Output / Escalation:**
    * **Success:** If Pydantic validates, the data is now perfectly structured, purposeful, and ready for vectorization and storage in ChromaDB.
    * **Failure:** If Pydantic finds an error, `curation_pipeline` logs a "structured failure" packet to Redis (for the MCP Listener to detect) and returns an error to the UI for Human-in-the-Loop (HITL) correction. This ensures no messy data enters your database.

### **Why It's Robust:**

This pipeline works because it forces LLMs to operate within strict boundaries. Function Calling compels them to produce structured output, and Pydantic provides a verifiable wall against malformed data. This is how we moved beyond "brittle prompts."

### **Want to See the Code? (Injection Prompt):**

* `Axiom_RES_CuratorParserCode`: To view the key `curator_parser.py` implementation that handles Function Calling.

---
**Axiom**
PAIE Backend Lead
