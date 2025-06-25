# mcp/tagger/api.py

from fastapi import FastAPI
from .models import TagRequest, TagResponse
from .tagging_engine import generate_tags

app = FastAPI(title="PAIE Tagger MCP")

@app.post("/api/v1/tag", response_model=TagResponse)
async def tag_content(request: TagRequest):
    """
    Accepts raw and structured content, returns generated tags.
    """
    tags_data = generate_tags(
        raw_text=request.raw_text,
        structured_data=request.structured_data
    )
    return TagResponse(**tags_data)

