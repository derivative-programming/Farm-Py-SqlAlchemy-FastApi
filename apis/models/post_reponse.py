# apis/models/post_reponse.py

"""
    #TODO add comment
"""

from typing import List
from pydantic import Field
from helpers.pydantic_serialization import CamelModel
from .validation_error import ValidationErrorItem


class PostResponse(CamelModel):
    """
        #TODO add comment
    """
    success: bool = Field(
        default=False,
        description="Success")

    message: str = Field(
        default="",
        description="Message")

    validation_errors: List[ValidationErrorItem] = Field(
        default_factory=list,
        description="Validation Errors")
