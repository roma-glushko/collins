import logging


def setup_logger(log_level=logging.DEBUG) -> None:
    # Create a custom logger
    logger = logging.root

    std_handler = logging.StreamHandler()
    std_handler.setLevel(log_level)

    std_format = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
    std_handler.setFormatter(std_format)

    logger.addHandler(std_handler)

    logger.info("Logger has been configured")
