# services/logging_config.py  # pylint: disable=duplicate-code

"""
This module provides configuration for logging in the application.
"""

import logging

# Define a proper date format string
DATE_FORMAT = "%Y-%m-%d %H:%M:%S"

# Configure the logging with a proper date format
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    datefmt=DATE_FORMAT
)


def get_logger(name):
    """
    Get a logger instance with the specified name.

    Args:
        name (str): The name of the logger.

    Returns:
        logging.Logger: The logger instance.
    """
    return logging.getLogger(name)
