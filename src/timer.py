import time
from logging import Logger
from typing import Any, Optional

from .logger import Color, get_logger


class Timer:
    """Calculating the time"""

    def __init__(self, prefix: str = "", logger: Optional[Logger] = None):
        self.logger = logger or get_logger("Timer")
        self.prefix = prefix
        self.start = -1

    def __enter__(self):
        self.start = time.time()
        self.logger.info(f"{Color.CYAN}%s... {Color.RESET}", self.prefix)

    def __exit__(self, *args: Any):
        used = time.time() - self.start
        self.logger.info(
            f"{Color.CYAN}%s {Color.WHITE}done. Used:"
            f" {Color.YELLOW}%.1fs{Color.WHITE}.{Color.RESET}",
            self.prefix,
            used,
        )
