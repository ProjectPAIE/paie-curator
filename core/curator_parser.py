# core/curator_parser.py (V3.0 - With "Fixer Function")

from langchain_community.llms import Ollama
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import JsonOutputParser
from pydantic import BaseModel
from typing import Type, Union, Dict, Any

from .config_loader import MODEL_CONFIG, OLLAMA_BASE_URL
from .logger_setup import logger

def _flatten_llm_output(raw_output: Dict[str, Any]) -> Dict[str, Any]:
    """
    The "Fixer Function." It checks for the nested 'properties' format
    and flattens it into the simple key-value format our Pydantic models expect.
    """
    if "properties" in raw_output and isinstance(raw_output["properties"], dict):
        logger.info("Nested JSON format detected. Flattening output...")
        flattened = {}
        for key, value_dict in raw_output["properties"].items():
            if isinstance(value_dict, dict) and "value" in value_dict:
                flattened[key] = value_dict["value"]
            else:
                flattened[key] = value_dict  # Keep it as is if format is unexpected
        return flattened
    return raw_output  # Return original if not nested

def parse_text_to_schema(text_input: str, pydantic_schema: Type[BaseModel]) -> Union[BaseModel, None]:
    """
    Takes raw text and a Pydantic schema and extracts the data. Includes a
    robust "fixer" function to handle nested JSON outputs from the LLM.
    """
    logger.info(f"Parser: Initiating extraction into '{pydantic_schema.__name__}' schema.")
    
    try:
        model_tag = MODEL_CONFIG.get('default_parser_model', 'phi3:latest')
        llm = Ollama(model=model_tag, base_url=OLLAMA_BASE_URL, format="json")
        
        parser = JsonOutputParser()

        template = """
        You are an expert at extracting structured information from user text.
        Based on the user's request below, populate the fields of the following JSON schema.
        Only output a single, valid JSON object.

        JSON Schema:
        {format_instructions}

        User Request:
        {user_request}
        """
        prompt = ChatPromptTemplate.from_template(
            template,
            partial_variables={"format_instructions": pydantic_schema.model_json_schema()}
        )
        
        chain = prompt | llm | parser
        
        logger.info(f"Parser: Invoking chain for schema '{pydantic_schema.__name__}'...")
        raw_result = chain.invoke({"user_request": text_input})
        
        # --- THE FIX ---
        # We now run the raw result through our fixer function before validation.
        flattened_result = _flatten_llm_output(raw_result)
        
        # Now we validate the clean, flattened data with Pydantic
        final_data = pydantic_schema(**flattened_result)
        
        logger.info("Parser: Successfully parsed and validated data.")
        return final_data

    except Exception as e:
        logger.error(f"Parser: Data parsing failed. Error: {e}", exc_info=True)
        return None
