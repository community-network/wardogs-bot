import logging
from logging.handlers import RotatingFileHandler
import sys


def setup_logger(logger: logging.Logger):
    logger.handlers.clear()
    logger.setLevel(logging.DEBUG)

    console_log_handler = logging.StreamHandler(sys.stdout)
    console_log_handler.setLevel(logging.INFO)

    file_log_handler = RotatingFileHandler(
        filename="discord.log",
        encoding="utf-8",
        maxBytes=32 * 1024 * 1024,  # 32 MiB
        backupCount=5,  # Rotate through 5 files
    )
    file_log_handler.setLevel(logging.DEBUG)
    dt_fmt = "%Y-%m-%d %H:%M:%S"

    formatter = logging.Formatter(
        "[{asctime}] [{levelname}] {name}: {message}", dt_fmt, style="{"
    )
    file_log_handler.setFormatter(formatter)
    console_log_handler.setFormatter(formatter)

    # logger.addHandler(file_log_handler) # for debugging
    logger.addHandler(console_log_handler)
