import logging


def setup_logging():
    """Configure the global logging system (call once at startup)."""
    logging.basicConfig(
        level = logging.INFO,
        format = '%(asctime)s - %(levelname)s - %(name)s - %(message)s',
        datefmt = '%H:%M:%S',
        force = True,
    )

logger = logging.getLogger("personal_screener")
