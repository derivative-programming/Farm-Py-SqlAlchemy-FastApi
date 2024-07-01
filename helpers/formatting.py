# helpers/formatting.py

"""
    This module provides helper functions for formatting strings.
"""
import re


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


def pascal_to_snake_case(pascal_str):
    """
    Convert a PascalCase string to snake_case.
    """
    # Find all uppercase letters and prepend them with
    # an underscore, except the first character
    snake_str = re.sub(r'(?<!^)(?=[A-Z])', '_', pascal_str)
    # Convert the entire string to lowercase
    snake_str = snake_str.lower()
    return snake_str
