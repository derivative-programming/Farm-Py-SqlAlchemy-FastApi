# helpers/formatting.py

"""
    This module provides helper functions for formatting strings.
"""


def snake_to_camel(snake_str: str) -> str:
    """
    Convert a snake_case string to camelCase.

    Args:
        snake_str (str): The snake_case string to convert.

    Returns:
        str: The camelCase string.

    Example:
        >>> snake_to_camel('hello_world')
        'helloWorld'
    """

    components = snake_str.split('_')
    # Capitalize the first letter of each component except the first one,
    # join them together, and prepend the first component.
    return components[0] + ''.join(x.capitalize() for x in components[1:])
