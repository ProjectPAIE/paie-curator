# core/curator_router.py (V3.0 - Sealed Build with IntentResult Schema)

from langchain_community.llms import Ollama
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import PydanticOutputParser
from pydantic import BaseModel, Field
from typing import Literal, Union

from .config_loader import MODEL_CONFIG, OLLAMA_BASE_URL
from .logger_setup import logger
from .fallback_manager import handle_fallback

class IntentResult(BaseModel):
    intent: Literal["INGEST", "QUERY", "UNKNOWN"]

def classify_intent(user_input: str) -> Union[IntentResult, None]:
    logger.info(f"Router: Classifying intent for input: '{user_input[:50]}...'")

    try:
        model_tag = MODEL_CONFIG.get('default_triage_model', 'phi3:latest')
        llm = Ollama(model=model_tag, base_url=OLLAMA_BASE_URL, format="json")
        parser = PydanticOutputParser(pydantic_object=IntentResult)

        template = """
        You are an expert routing agent. Classify the user's intent as INGEST, QUERY, or UNKNOWN.
        Respond with only the appropriate JSON object based on the schema.

        {format_instructions}

        User Request:
        {user_request}
        """
        prompt = ChatPromptTemplate.from_template(
            template,
            partial_variables={"format_instructions": parser.get_format_instructions()}
        )
        
        chain = prompt | llm | parser
        logger.info("Router: Invoking intent classification chain...")
        result = chain.invoke({"user_request": user_input})
        logger.info(f"Router: Classified intent as: {result.intent}")
        return result

    except Exception as e:
        logger.error(f"An exception occurred during intent classification: {e}", exc_info=True)
        handle_fallback(reason="PARSING_ERROR", user_input=user_input, module_origin="curator_router", llm_output=str(e))
        return None
