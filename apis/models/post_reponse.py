# apis/models/post_reponse.py

"""
    #TODO add comment
"""

from helpers.pydantic_serialization import CamelModel,SnakeModel
from .validation_error import ValidationErrorItem
from typing import List
from pydantic import Field


class PostResponse(CamelModel):
    success: bool = Field(default=False,description="Success")
    message: str = Field(default="",description="Message")
    validation_errors: List[ValidationErrorItem] = Field(default_factory=list, description="Validation Errors")
