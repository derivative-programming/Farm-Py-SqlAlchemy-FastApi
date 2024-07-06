# apis/models/validation_error.py  # pylint: disable=duplicate-code

"""
This module contains the definition of the ValidationErrorItem class.

The ValidationErrorItem class is a Pydantic model
that represents an item in a validation error.
It contains the property and message attributes,
which provide information about the validation error.
"""

from pydantic import Field

from helpers.pydantic_serialization import CamelModel


class ValidationErrorItem(CamelModel):
    """
    Represents an item in a validation error.

    Attributes:
        property (str): The property associated with the validation error.
        message (str): The error message describing the validation error.
    """

    property: str = Field(
        default="",
        description="Property")

    message: str = Field(
        default="",
        description="Message")
