# mcp/tagger/tests/test_tagger.py

from fastapi.testclient import TestClient
from mcp.tagger.api import app

client = TestClient(app)

def test_tagging_endpoint():
    payload = {
        "raw_text": "A beautiful new mural by Don Guicho appears downtown.",
        "structured_data": {
            "title": "Downtown Mural",
            "category": "Mural",
            "location": "Public Plaza"
        }
    }

    response = client.post("/api/v1/tag", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert "tags" in data
    assert isinstance(data["tags"], list)
    assert any(tag["tag"] == "Don Guicho" for tag in data["tags"])
