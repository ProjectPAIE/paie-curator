# mcp/tagger/tagging_engine.py

from typing import Dict, List
from .models import TagConfidence

def generate_tags(raw_text: str, structured_data: Dict) -> Dict:
    """
    Placeholder implementation — returns dummy tags.
    Replace with real LLM-based logic in Phase 2.
    """
    dummy_tags = [
        TagConfidence(tag="art", confidence=0.95),
        TagConfidence(tag="mural", confidence=0.91),
        TagConfidence(tag="public space", confidence=0.87),
        TagConfidence(tag="Don Guicho", confidence=0.99)  # 👋 wink to the family
    ]
    return {"tags": dummy_tags}
