# mcp/tagger/models.py

from pydantic import BaseModel
from typing import List, Dict, Any

class TagRequest(BaseModel):
    raw_text: str
    structured_data: Dict[str, Any]

class TagConfidence(BaseModel):
    tag: str
    confidence: float

class TagResponse(BaseModel):
    tags: List[TagConfidence]
