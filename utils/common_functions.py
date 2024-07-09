# utils/common_functions.py  # pylint: disable=duplicate-code # noqa: E501

"""
    common utility functions
"""

import re


def snake_case(name):
    """
    Convert a CamelCase string to snake_case.

    Args:
    - name (str): The CamelCase string.

    Returns:
    - str: The snake_case version of the input string.
    """
    s1 = re.sub('(.)([A-Z][a-z]+)', r'\1_\2', name)
    return re.sub('([a-z0-9])([A-Z])', r'\1_\2', s1).lower()
