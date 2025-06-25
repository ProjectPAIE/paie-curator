# core/schema_selector.py (V3.2 - Docker-Aware, Patch-Only)
from langchain_community.llms import Ollama
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from typing import List, Type
from pydantic import BaseModel

from .config_loader import MODEL_CONFIG, OLLAMA_BASE_URL  # ✅ FIXED IMPORT
from .logger_setup import logger
from .schemas import ArtEvent, DJMix, Recipe, VehicleLog, PersonNote, FreeNoteCard

# This dictionary maps the exact class name to the class itself.
SCHEMA_TOOLBELT = {
    "ArtEvent": ArtEvent,
    "DJMix": DJMix,
    "Recipe": Recipe,
    "VehicleLog": VehicleLog,
    "PersonNote": PersonNote
}

def select_schema(text_input: str) -> Type[BaseModel]:
    """
    Analyzes input text and selects the most appropriate Pydantic schema
    by providing the model with the full schema names and their docstring descriptions.
    Uses FreeNoteCard as a guaranteed fallback.
    """
    logger.info(f"Schema Selector V3.2: Initiating for input: '{text_input[:50]}...'")
    
    try:
        model_tag = MODEL_CONFIG.get('default_triage_model', 'phi3')
        llm = Ollama(model=model_tag, base_url=OLLAMA_BASE_URL)  # ✅ PATCH INJECTION

        # Create a formatted list of schema names for the prompt
        tool_names = list(SCHEMA_TOOLBELT.keys())
        
        prompt_template = f"""
        Based on the user's text below, which of the following tools is the most appropriate one to use?
        Respond with only the single, exact name of the best tool from the 'Available Tools' list. Do not add any other text.

        Available Tools:
        {", ".join(tool_names)}

        User Text: "{text_input}"

        Best Tool Name:
        """
        
        prompt = ChatPromptTemplate.from_template(prompt_template)
        chain = prompt | llm | StrOutputParser()
        
        logger.info("Invoking schema selection chain...")
        llm_choice_str = chain.invoke({"text": text_input}).strip()
        logger.info(f"LLM chose: '{llm_choice_str}'")

        # Look up the chosen tool name in our toolbelt dictionary.
        selected_schema = SCHEMA_TOOLBELT.get(llm_choice_str)
        
        if selected_schema:
            logger.info(f"Successfully matched to schema: {selected_schema.__name__}")
            return selected_schema

        # If the LLM hallucinates a name that isn't in our toolbelt, we use our safety net.
        logger.warning(f"Could not match LLM choice '{llm_choice_str}' to an available schema. Defaulting to FreeNoteCard.")
        return FreeNoteCard

    except Exception as e:
        logger.error(f"An exception occurred during schema selection: {e}", exc_info=True)
        return FreeNoteCard