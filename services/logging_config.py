# logging_config.py

"""
    #TODO add comment
"""

import logging

logging.basicConfig(level=logging.INFO)


def get_logger(name):
    """
    #TODO add comment
    """
    return logging.getLogger(name)
