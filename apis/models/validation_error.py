# apis/models/validation_error.py

"""
    #TODO add comment
"""

from helpers.pydantic_serialization import CamelModel, SnakeModel
from pydantic import Field


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
