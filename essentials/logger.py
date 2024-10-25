# logger_setup.py
import logging
import colorlog


def setup_logger():
    """Setup and initiate the logger."""
    
    logger = logging.getLogger("openrwds")
    logger.setLevel(logging.INFO)

    if not logger.handlers:  # Check if handlers already exist to avoid duplicates
        # Console handler (with color)
        console_handler = logging.StreamHandler()
        color_formatter = colorlog.ColoredFormatter(
            "%(log_color)s%(asctime)s:%(levelname)s:%(name)s: %(message)s",
            datefmt="%Y-%m-%d %H:%M:%S",
            log_colors={
                "DEBUG": "cyan",
                "INFO": "green",
                "WARNING": "yellow",
                "ERROR": "red",
                "CRITICAL": "bold_red",
            },
        )
        console_handler.setFormatter(color_formatter)

        # File handler (no color)
        file_handler = logging.FileHandler("app.log")
        file_formatter = logging.Formatter(
            "%(asctime)s:%(levelname)s:%(name)s: %(message)s",
            datefmt="%Y-%m-%d %H:%M:%S",
        )
        file_handler.setFormatter(file_formatter)

        # Add both handlers
        logger.addHandler(console_handler)
        logger.addHandler(file_handler)

    return logger
