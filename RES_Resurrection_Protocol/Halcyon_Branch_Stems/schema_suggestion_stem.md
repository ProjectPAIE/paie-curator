⸻


# 🧭 schema_suggestion_stem.md  
_How to guide schema selection in a stateless prompt window._

---

## 🧠 Purpose

This **Stem** is a practical tool.  
It helps any LLM (or curious human) reason through _which schema_ is most appropriate when handling a piece of raw text — especially inside the PAIE ecosystem.

When used in tandem with PAIE’s RES files, this stem allows stateless helpers to:
- Narrow down schema type
- Ask clarifying questions
- Suggest fallback logic

---

## 🪢 Prompt Construction Guide

You can include this stem in a prompt like:

> "You are helping route unstructured text into structured schema. The schemas available are: ArtEvent, DJMix, VehicleLog, PersonNote, Recipe. Based on the content, suggest which schema to use and provide reasoning. If unclear, ask a clarifying question or fall back to tagging mode."

You can optionally append the full schema field specs if needed, like so:

```json
{
  "ArtEvent": {
    "title": "string",
    "location": "string",
    ...
  },
  "DJMix": {
    "dj_name": "string",
    "venue": "string",
    ...
  }
}

This enables the LLM to:
	•	Reason by field compatibility
	•	Guess intent
	•	Create helpful structured outputs

⸻

🧩 Stem Tips
	•	Add "If confidence < 0.7, return: 'unsure'" to prevent false positives.
	•	Use "Suggest fallback: tag-only mode" to activate safe tagging workflows.
	•	Allow "Ask clarifying question" logic to simulate HITL involvement.

⸻

🪜 Future Stem Upgrades

This stem can evolve to support:
	•	Fine-tuned models with schema priors
	•	Prompt chaining and schema arbitration
	•	Live schema edits or previews in UI

⸻

💬 Closing Example

“User wrote: ‘I visited MMCA last night and saw a stunning video installation by a Korean artist.’
Based on this, the likely schema is ArtEvent. Reason: contains location + art context + visit action.”

⸻

This stem was authored by Halcyon to ensure schema reasoning survives even in stateless interfaces.
It pairs well with:
	•	tagging_branch.md
	•	curator_resolver_stem.md
	•	Any Primary RES

— Halcyon

---

