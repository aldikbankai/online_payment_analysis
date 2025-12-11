# logger_config.py
import logging
import os

# Логтар сақталатын папка
if not os.path.exists("logs"):
    os.mkdir("logs")

LOG_FILE = "logs/app.log"

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(module)s | %(message)s",
    handlers=[
        logging.FileHandler(LOG_FILE, encoding="utf-8"),
        logging.StreamHandler()      # консольге шығару
    ]
)

logger = logging.getLogger(__name__)