# apis/models/validation_error.py

"""
    #TODO add comment
"""

from pydantic import Field

from helpers.pydantic_serialization import CamelModel


class ValidationErrorItem(CamelModel):
    """
    #TODO add comment
    """

    property: str = Field(
        default="",
        description="Property")

    message: str = Field(
        default="",
        description="Message")
