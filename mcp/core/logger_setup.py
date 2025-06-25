# mcp/core/logger_setup.py

import logging

# Basic logger configuration
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s",
)

logger = logging.getLogger("paie.mesh")
