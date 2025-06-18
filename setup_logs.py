import os
import logging
from dotenv import load_dotenv

load_dotenv()

LOG_DIR = os.getenv("LOG_DIR", "logs")
LOG_FILE = os.getenv("LOG_FILE", "app.log")
LOG_LEVEL = os.getenv("LOG_LEVEL", "DEBUG").upper()


def setup_logging():
    # Remove old log file
    log_path = os.path.join(LOG_DIR, LOG_FILE)
    if os.path.exists(log_path):
        os.remove(log_path)

    os.makedirs(LOG_DIR, exist_ok=True)

    logger = logging.getLogger()
    logger.setLevel(logging.DEBUG)  # Capture all; handlers will filter

    # Console handler (show everything)
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.DEBUG)
    console_format = logging.Formatter("%(levelname)-8s | %(message)s")
    console_handler.setFormatter(console_format)
    logger.addHandler(console_handler)

    # File handler (record WARNING+ only)
    file_handler = logging.FileHandler(log_path)
    file_handler.setLevel(logging.WARNING)
    file_format = logging.Formatter("%(asctime)s | %(levelname)-8s | %(message)s")
    file_handler.setFormatter(file_format)
    logger.addHandler(file_handler)

    # Write one log at each level
    logger.debug("Debug message: diagnostic info.")
    logger.info("Info message: app startup complete.")
    logger.warning("Warning message: risky behavior.")
    logger.error("Error message: something failed.")
    logger.critical("Critical message: app is in danger.")


if __name__ == "__main__":
    setup_logging()
    print(f"Logs written to: {os.path.join(LOG_DIR, LOG_FILE)}")
