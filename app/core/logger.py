import logging
from loguru import logger

# Configure logger
logger.remove()
logger.add(
    sink="logs/application.log",
    format="{time:YYYY-MM-DD at HH:mm:ss} | {level} | {message}",
    level="INFO",
)

# Configure logging for Flask
logging.getLogger("werkzeug").setLevel(logging.WARNING)
