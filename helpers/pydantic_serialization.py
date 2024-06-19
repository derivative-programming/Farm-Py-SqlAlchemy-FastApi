# helpers/pydantic_serialization.py

"""
This module provides helper functions and classes for Pydantic serialization.
"""

import re
from pydantic import BaseModel


def to_camel(string: str) -> str:
    """
    Convert a snake_case string to camelCase.

    Args:
        string (str): The snake_case string to be converted.

    Returns:
        str: The camelCase string.

    """
    return ''.join(
        word.capitalize() if i else word
        for i, word in enumerate(string.split('_'))
    )


def to_snake(string: str) -> str:
    """
    Convert a camelCase string to snake_case.

    Args:
        string (str): The camelCase string to be converted.

    Returns:
        str: The snake_case string.

    """
    string = re.sub('(.)([A-Z][a-z]+)', r'\1_\2', string)
    return re.sub('([a-z0-9])([A-Z])', r'\1_\2', string).lower()


class CamelModel(BaseModel):
    """
    A Pydantic BaseModel that converts snake_case field names to camelCase.

    Configures Pydantic to use the aliases in the generated
    schema and when parsing and serializing data.

    """

    class Config:
        """
        Configuration class for CamelModel.

        """

        alias_generator = to_camel
        populate_by_name = True


class SnakeModel(BaseModel):
    """
    A Pydantic BaseModel that converts camelCase field names to snake_case.

    Configures Pydantic to use the aliases in the generated schema
    and when parsing and serializing data.

    """

    class Config:
        """
        Configuration class for SnakeModel.

        """

        alias_generator = to_snake
        populate_by_name = True
