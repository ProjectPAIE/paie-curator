# mcp/core/mesh_controller.py
# This is the master orchestrator for the Model Context Protocol (MCP).
# It coordinates the flow of data between different agents and services.

import httpx # A modern, asynchronous HTTP client
from typing import Dict, Any

# We will eventually import our other agents and tools here
# from .tagger import tag_content 
from ..core.logger_setup import logger

# We will get this from a config file later. For now, it's hardcoded.
TAGGER_API_URL = "http://localhost:8002/api/v1/tag" 

async def run_ingestion_mesh(raw_text: str) -> Dict[str, Any]:
    """
    The main entry point for the MCP ingestion workflow.
    It takes raw text, gets tags from the tagger, and prepares the final data packet.
    """
    logger.info(f"MCP Controller: Initiating ingestion for text: '{raw_text[:50]}...'")

    # Step 1: Call our sealed Tagger MCP to get structured tags.
    # We use an async HTTP client to make the API call.
    try:
        logger.info(f"Calling Tagger MCP at {TAGGER_API_URL}...")
        async with httpx.AsyncClient() as client:
            response = await client.post(TAGGER_API_URL, json={"text": raw_text})
            response.raise_for_status() # Raises an exception for 4xx/5xx errors
            tagger_output = response.json()
        
        logger.info(f"Received response from Tagger: {tagger_output}")

    except httpx.RequestError as e:
        logger.error(f"MCP Controller: Failed to connect to Tagger MCP. Error: {e}", exc_info=True)
        # In a real scenario, we would trigger our fallback_manager here.
        return {"status": "error", "message": "Could not connect to the Tagger service."}
    except Exception as e:
        logger.error(f"MCP Controller: An unexpected error occurred. Error: {e}", exc_info=True)
        return {"status": "error", "message": "An unknown error occurred in the mesh."}


    # Step 2 (Future): Pass the tagged data to the next agent in the chain
    # For now, we just return the successful output.
    final_data_packet = {
        "original_text": raw_text,
        "curated_tags": tagger_output.get("tags", []),
        "source_fields": tagger_output.get("source_fields", {}),
        "status": "curated_and_tagged"
    }

    logger.info("MCP Controller: Ingestion mesh completed successfully.")
    return final_data_packet
