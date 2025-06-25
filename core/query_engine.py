# core/query_engine.py (V2.2 - Docker-Aware + Robust Filter Handling)
import chromadb
from typing import List, Union, Dict

from .config_loader import DB_CONFIG, OLLAMA_BASE_URL
from .logger_setup import logger
from langchain_community.llms import Ollama
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

def run_query_pipeline(question: str, model_to_use: str, query_filter: Dict = None) -> str:
    """
    This is the full RAG pipeline. It takes a question and a filter,
    retrieves context, and then calls an LLM to generate an answer.
    """
    logger.info(f"Starting RAG pipeline for question: '{question}'")
    
    # 1. Retrieve documents from the database
    try:
        chroma_client = chromadb.HttpClient(host=DB_CONFIG.get('host'), port=DB_CONFIG.get('port'))
        collection_name = DB_CONFIG.get('collection_name', 'paie_main_storage')
        collection = chroma_client.get_collection(name=collection_name)

        # --- THIS IS THE CORRECTED LOGIC ---
        if query_filter:
            logger.info(f"Querying collection '{collection_name}' with filter: {query_filter}...")
            results = collection.query(query_texts=[question], n_results=5, where=query_filter)
        else:
            logger.info(f"Querying collection '{collection_name}' with no filter...")
            results = collection.query(query_texts=[question], n_results=5)
        # --- END OF CORRECTION ---
        
        retrieved_documents = results['documents'][0]
        if not retrieved_documents:
            logger.warning(f"No documents found for query.")
            return "I could not find any relevant documents in the knowledge base to answer your question."
            
        context_string = "\n\n---\n\n".join(retrieved_documents)
    except Exception as e:
        logger.error(f"An error occurred during database query: {e}", exc_info=True)
        return "Error: Could not connect to or query the knowledge base."

    # 2. Get the final answer from the LLM
    try:
        logger.info(f"Sending context and question to the LLM: {model_to_use}")
        template = """
        You are an assistant for question-answering tasks. Use the following pieces of retrieved context to answer the question. 
        If you don't know the answer or the context isn't relevant, just say that you don't know. Be concise.
        Context: {context}
        Question: {question}
        Helpful Answer:
        """
        prompt = ChatPromptTemplate.from_template(template)
        llm = Ollama(model=model_to_use, base_url=OLLAMA_BASE_URL)
        chain = prompt | llm | StrOutputParser()
        answer = chain.invoke({"context": context_string, "question": question})
        logger.info("Successfully received answer from LLM.")
        return answer
    except Exception as e:
        logger.error(f"An error occurred while calling the LLM: {e}", exc_info=True)
        return "Error: Could not get a response from the language model."