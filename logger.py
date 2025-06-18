import os
import logging
from dotenv import load_dotenv

load_dotenv()


def configure_logging():
    log_dir = os.getenv("LOG_DIR", "logs")
    log_file = os.getenv("LOG_FILE", "app.log")
    os.makedirs(log_dir, exist_ok=True)

    # Root logger
    logger = logging.getLogger()
    logger.setLevel(logging.DEBUG)  # Set to lowest to allow filtering per handler

    # Console handler (everything)
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.DEBUG)
    console_format = logging.Formatter("%(levelname)-8s | %(message)s")
    console_handler.setFormatter(console_format)
    logger.addHandler(console_handler)

    # File handler (warnings and above only)
    file_handler = logging.FileHandler(os.path.join(log_dir, log_file))
    file_handler.setLevel(logging.WARNING)
    file_format = logging.Formatter("%(asctime)s | %(levelname)-8s | %(message)s")
    file_handler.setFormatter(file_format)
    logger.addHandler(file_handler)

    # Silence werkzeug logs going to file (avoid bloated log file)
    logging.getLogger("werkzeug").setLevel(logging.INFO)
