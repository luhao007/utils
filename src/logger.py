"""Utility functions for logging and timing execution."""

import logging


class Color:
    """ANSI color codes for terminal output."""

    RED = "\033[91m"
    GREEN = "\033[92m"
    YELLOW = "\033[93m"
    BLUE = "\033[94m"
    MAGENTA = "\033[95m"
    CYAN = "\033[96m"
    WHITE = "\033[97m"
    RESET = "\033[0m"


def get_logger(name: str) -> logging.Logger:
    """
    Get a logger with nice color formatting.

    Args:
        name: Logger name (typically __name__)

    Returns:
        A configured logger with color formatting
    """
    logger = logging.getLogger(name)

    # Only add handler if this logger doesn't have one
    if not logger.handlers:
        handler = logging.StreamHandler()
        formatter = logging.Formatter(
            f"{Color.WHITE}%(asctime)s {Color.YELLOW}%(name)s"
            f" {Color.GREEN}%(levelname)s {Color.WHITE}- %(message)s"
        )
        handler.setFormatter(formatter)
        logger.addHandler(handler)

    # Inherit level from root logger if it's set
    root_logger = logging.getLogger()
    if root_logger.level != logging.NOTSET:
        logger.setLevel(root_logger.level)

    logger.propagate = False
    return logger
