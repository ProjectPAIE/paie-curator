# main.py (V1.1 - With Structured Fallback)
import sys
from pathlib import Path
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Any

# Add project root to the path to allow imports from core
sys.path.append(str(Path(__file__).parent))

try:
    from core.curation_pipeline import process_user_input
    from core.logger_setup import logger
except ImportError as e:
    print(f"FATAL ERROR: Could not import backend modules. {e}")
    sys.exit(1)

# --- API Request Models ---
class IngestRequest(BaseModel):
    text: str
    source: str = "ui_capture"

# --- FastAPI Application ---
app = FastAPI(
    title="Project PAIE Curation Service",
    description="A modular, resilient ingestion and curation engine.",
    version="1.0.0"
)

@app.get("/")
def read_root():
    return {"status": "PAIE Curation Engine is online."}

@app.post("/api/v1/curate")
async def curate_note(request: IngestRequest):
    """
    The primary endpoint for the MVP. It takes raw text and processes it
    through the full ingestion pipeline.
    """
    logger.info(f"API: Received /curate request for text: '{request.text[:50]}...'")
    try:
        pipeline_result = process_user_input(request.text)
        
        # --- THIS IS THE FIX ---
        # The pipeline now returns a structured dictionary for both success and failure.
        # We simply return that directly to the frontend.
        return pipeline_result

    except Exception as e:
        logger.error(f"API /curate endpoint CRITICAL error: {e}", exc_info=True)
        # This is a true server error, not a planned fallback.
        raise HTTPException(status_code=500, detail="An unexpected critical error occurred.")
