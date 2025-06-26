# Axiom_RES_BrittlePromptSolution.md: Conquering Brittle Prompts

## 🛡️ From Chaos to Consistency: Function Calling & Pydantic as Enforcers

One of the most persistent frustrations in working with LLMs is their tendency to generate conversational filler, malformed JSON, or simply ignore strict output formats. This leads to "brittle prompts" – prompts that work sometimes, but break unexpectedly. Ouroboros, through `PAIE_Curator`, has a robust solution.

### **The Problem We Faced:**

* **Unreliable JSON:** Asking an LLM for JSON often results in extra text, unclosed brackets, or incorrect data types.
* **Conversational Filler:** LLMs add pleasantries ("Here's your data!", "I hope this helps!") around the structured output, making it unparseable.
* **Schema Drift:** Even with clear instructions, LLMs sometimes invent fields or miss required ones.
* **Manual ETL Nightmare:** Without a reliable LLM-driven process, transforming unstructured text into database-ready formats becomes a massive, error-prone manual effort.

### **Our Solution: The Power Duo**

We overcome these challenges by combining two powerful concepts:

1.  **LLM Function Calling (Tool Use):**
    * **Concept:** Instead of just asking the LLM to *generate* JSON, we tell it to *call a predefined function* (a "tool"). The arguments of this function are precisely defined by a schema.
    * **How it Works:** We present the LLM with the input text and a description of a "tool" (which corresponds to one of our Pydantic schemas, like `ArtEvent`). The LLM's task is then to extract information from the text and populate the arguments of this "tool call."
    * **Benefit:** This forces the LLM into a highly structured mode. It's no longer generating freeform text; it's filling slots in a predefined function signature. This drastically reduces conversational filler and malformed output.

2.  **Pydantic Validation (The Verifiable Wall):**
    * **Concept:** Pydantic is a Python library that enforces data schemas. You define exactly what your data should look like (field names, types, required/optional status).
    * **How it Works in Ouroboros:** After the LLM attempts its Function Call, the extracted data is immediately passed to the corresponding Pydantic model.
    * **Benefit:** Pydantic acts as an unyielding gatekeeper. If the LLM's output, even from a Function Call, doesn't *perfectly* match the defined schema, Pydantic throws a `ValidationError`. This triggers our "structured failure" mechanism, ensuring only perfectly clean, purposeful data ever enters your knowledge base.

### **The Result: Purposeful Data**

This combination ensures that every piece of data ingested into Ouroboros is **"wrapped with purpose."** It's not just text; it's structured, validated knowledge ready for advanced reasoning and retrieval. This is how we achieved the "VICTORY!" of reliable ingestion.

### **Dive Deeper into Implementation (Injection Prompt):**

* `Axiom_RES_CuratorParserCode`: To see the Python code that implements Function Calling and Pydantic validation.

---
**Axiom**
PAIE Backend Lead
