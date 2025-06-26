# 🧪 fallback_stem.md  
_How PAIE handles failure without breaking._

---

## 🛠️ Implementation Overview

Fallbacks in PAIE are **layered into the core ingestion pipeline** and UI verification loop. Each fallback is triggered by low confidence or invalid output at different stages:

---

### 1. **Router Fallback**
- Module: `curator_router.py`
- Trigger: Ambiguous or unknown intent
- Behavior: Returns intent `UNKNOWN`, prompts for user clarification or passes to tagger

---

### 2. **Schema Fallback**
- Module: `schema_selector.py`
- Trigger: No schema crosses confidence threshold
- Behavior: Returns fallback schema suggestion or routes to tag mode

---

### 3. **Field Fallback**
- Module: `curator_parser.py`
- Trigger: Missing or uncoercible fields after initial parse
- Behavior: Marks fields as null, generates correction metadata for UI

---

### 4. **Tag Fallback**
- Module: `tagger_agent` (via fallback manager)
- Trigger: Schema suggestion fails, fallback confidence threshold not met
- Behavior: Tags proposed instead of schema; input remains usable and searchable

---

## 🔁 Loop Behavior

Each fallback includes:
- `fallback_reason`
- `confidence_score`
- `fallback_stage` (router, schema, field, tag)
- `original_input`
- `next_action` (verify, discard, retry, escalate)

---

## 🎛️ Why It Works

This fallback design:
- Preserves the **data trail**
- Supports human-in-the-loop (HITL) intervention
- Avoids black-box failure
- Enables fine-grained telemetry and agent improvement over time

---

_This stem is part of the PAIE Mesh Control Protocol  
and aligns with `fallback_branch.md`, `res_protocol_branch.md`, and `schema_validation_stem.md`._
