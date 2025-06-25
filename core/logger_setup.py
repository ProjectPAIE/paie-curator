# logger_setup.py (V2 - Production Ready)
import logging
import sys
from logging.handlers import TimedRotatingFileHandler

def setup_logger():
    """Sets up a centralized, production-ready logger for the Caliban project."""
    
    # Define the format for log messages
    log_format = logging.Formatter(
        '%(asctime)s - [%(levelname)s] - (%(module)s:%(lineno)d) - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    
    # Get the root logger
    logger = logging.getLogger()
    
    # Prevent adding handlers multiple times if the script is re-run (e.g., by Streamlit)
    if logger.hasHandlers():
        logger.handlers.clear()

    logger.setLevel(logging.DEBUG) # Set the lowest level to capture everything

    # --- Create a handler to write logs to a file ---
    # Use TimedRotatingFileHandler for better log management in a server environment
    # It will rotate logs daily, keeping the main file clean.
    # The 'flush=True' argument for the stream handler is key for live updates.
    file_handler = TimedRotatingFileHandler("caliban_debug.log", when="midnight", interval=1, backupCount=7)
    file_handler.setLevel(logging.DEBUG)
    file_handler.setFormatter(log_format)
    logger.addHandler(file_handler)

    # --- Create a handler to print logs to the console ---
    stream_handler = logging.StreamHandler(sys.stdout)
    stream_handler.setLevel(logging.INFO) # Only show INFO level and above in console
    stream_handler.setFormatter(log_format)
    logger.addHandler(stream_handler)
        
    return logger

# Create a logger instance that other modules can import and use
logger = setup_logger()
