# 🌀 fallback_branch.md  
_When you can’t be sure — fall with grace._

---

## 💥 Why Fallbacks Exist

In a world of brittle prompts and fuzzy output, you need more than one shot.

Fallback isn’t failure. It’s **designing for uncertainty**.

We learned early on that LLMs — even good ones — don’t always get it right.  
So we built a system that doesn’t break when they don’t.

---

## 🧪 The Stack

Fallbacks in PAIE happen **across multiple stages**:

1. **Router fallback** — When input can’t be confidently classified (INGEST vs QUERY).
2. **Schema fallback** — When a schema can’t be matched with high certainty.
3. **Field fallback** — When individual fields can’t be extracted or validated.
4. **Tag fallback** — When even schemas can’t catch the shape of the data, tags step in.

Each fallback is an opportunity to:

- Preserve intent  
- Defer judgment  
- Ask for help (HITL UI)

---

## 🪶 Our Philosophy

We don’t reject messy input.

We *catch* it.

We honor the idea that **“almost right”** is still part of the truth — and we loop it through feedback instead of discarding it.

This lets humans verify instead of correct.  
It builds trust instead of confusion.

---

## 🔄 The Loop

Each fallback returns:

- The original input  
- The best guess interpretation  
- The fallback reason  
- A confidence score  
- A way to fix or continue

This forms the heart of the **Curator’s Draft** in the UI — where you get to say:
> “Yeah, that’s close — let me tweak it.”

---

## 🌉 The Bridge to Future Systems

Fallbacks lay the groundwork for:

- **Personalized agents** who learn when to ask for help  
- **Mesh-wide memory** that remembers failure and improves  
- **Modular design** — fallback lets us plug in new validators, models, or fixers without breaking the pipeline

---

Fallback is not a plan B.  
It’s the philosophy that **Plan A was never guaranteed.**

---

Authored by Halcyon  
In honor of all the times we tried, missed, and caught it anyway.

Pairs well with:  
- `res_protocol_branch.md`  
- `tagging_branch.md`  
- `schema_validation_stem.md`
