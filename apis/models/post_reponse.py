# apis/models/post_reponse.py

"""
This module contains the definition of the PostResponse class.

The PostResponse class is a Pydantic model that represents
the response returned by the API when creating a post.

Attributes:
    success (bool): Indicates whether the operation was successful.
    message (str): A message associated with the response.
    validation_errors (List[ValidationErrorItem]):
        A list of validation errors, if any.

"""

from typing import List
from pydantic import Field
from helpers.pydantic_serialization import CamelModel
from .validation_error import ValidationErrorItem


class PostResponse(CamelModel):
    """
    Represents the response returned by the API when creating a post.

    Attributes:
        success (bool): Indicates whether the operation was successful.
        message (str): A message associated with the response.
        validation_errors (List[ValidationErrorItem]):
            A list of validation errors, if any.

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
