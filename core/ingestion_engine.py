# core/ingestion_engine.py

import chromadb
import uuid
from pydantic import BaseModel
from .config_loader import DB_CONFIG
from .logger_setup import logger

def save_structured_data(original_text: str, structured_data: BaseModel) -> str:
    """
    Takes a Pydantic object, prepares its metadata, and saves the original text
    to ChromaDB with the rich metadata attached.
    Returns the unique ID of the newly saved document.
    """
    if not DB_CONFIG:
        logger.error("Database configuration is missing. Cannot save.")
        return None

    try:
        logger.info(f"Saving curated data to ChromaDB...")
        client = chromadb.HttpClient(host=DB_CONFIG.get('host'), port=DB_CONFIG.get('port'))
        collection = client.get_collection(name=DB_CONFIG.get('collection_name'))

        # Prepare data for ChromaDB
        unique_id = str(uuid.uuid4())
        document_to_save = original_text
        metadata_to_save = structured_data.model_dump()

        # Clean up metadata for ChromaDB
        for key, value in metadata_to_save.items():
            if isinstance(value, list):
                metadata_to_save[key] = ', '.join(str(v) for v in value if v is not None)
            elif value is None:
                metadata_to_save[key] = ''

        collection.add(
            ids=[unique_id],
            documents=[document_to_save],
            metadatas=[metadata_to_save]
        )

        logger.info(f"Successfully saved document with ID: {unique_id}")
        return unique_id

    except Exception as e:
        logger.error(f"Failed to save data to ChromaDB: {e}", exc_info=True)
        return None

def ingest_text(text: str, source_name: str, custom_metadata: dict):
    """
    Compatibility shim for finalize_ingestion route.
    Wraps custom_metadata in a fallback schema and delegates to save_structured_data.
    """
    try:
        from core.schemas import GenericSchema
        wrapped = GenericSchema(**custom_metadata)
        return save_structured_data(original_text=text, structured_data=wrapped)
    except Exception as e:
        logger.error(f"Failed to ingest text using fallback schema: {e}", exc_info=True)
        return None
