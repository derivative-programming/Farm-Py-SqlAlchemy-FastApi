# services/logging_config.py

"""
    #TODO add comment
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
    #TODO add comment
    """
    return logging.getLogger(name)
