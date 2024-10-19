from essentials import config
import logging
import colorlog


def setup_logging():
    configurationManager = config.ConfigurationManager()
    defaultConfig = configurationManager.getBotConfig()

    if defaultConfig["LOGGING"] is True:
        logger = logging.getLogger("nextcord")
        logger.setLevel(logging.INFO)

        handler = logging.StreamHandler()
        file_handler = logging.FileHandler("app.log")

        formatter = colorlog.ColoredFormatter(
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

        handler.setFormatter(formatter)
        logger.addHandler(handler)
        logger.addHandler(file_handler)

        logger.info("Logging with colored output is set up successfully.")


if __name__ == "__main__":
    setup_logging()
