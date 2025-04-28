import logging
import sys
from typing import Any

import structlog


def configure_logger() -> structlog.BoundLogger:
    """
    Configure and return a structlog logger with JSON formatting.
    """
    # Configure structlog
    structlog.configure(
        processors=[
            structlog.contextvars.merge_contextvars,
            structlog.processors.add_log_level,
            structlog.processors.StackInfoRenderer(),
            structlog.dev.set_exc_info,
            structlog.processors.TimeStamper(fmt="iso"),
            structlog.processors.JSONRenderer(),
        ],
        wrapper_class=structlog.make_filtering_bound_logger(logging.INFO),
        context_class=dict,
        logger_factory=structlog.PrintLoggerFactory(),
        cache_logger_on_first_use=True,
    )

    # Configure standard library logging
    logging.basicConfig(format="%(message)s", stream=sys.stdout, level=logging.INFO)

    return structlog.get_logger()


# Create a global logger instance
logger = configure_logger()
