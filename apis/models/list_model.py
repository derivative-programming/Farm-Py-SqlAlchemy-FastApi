# apis/models/list_model.py  # pylint: disable=duplicate-code # noqa: E501

"""
This module contains the ListModel class, which represents a
list of items with pagination and sorting information.
"""

from typing import List
from pydantic import Field
from helpers.pydantic_serialization import CamelModel
from .validation_error import ValidationErrorItem


class ListModel(CamelModel):
    """
    Represents a list of items with pagination and sorting information.

    Attributes:
        page_number (int): The page number of the list.
        item_count_per_page (int): The number of items per page.
        order_by_column_name (str): The column
            name to order the list by.
        order_by_descending (bool): Indicates
            whether the list should be ordered in descending order.
        success (bool): Indicates whether the operation was successful.
        records_total (int): The total number of records in the list.
        records_filtered (int): The number of records filtered in the list.
        message (str): A message associated with the list.
        app_version (str): The version of the application.
        validation_errors (List[ValidationErrorItem]): A list
            of validation errors, if any.
    """

    page_number: int = Field(
        default=0,
        description="Page Number")

    item_count_per_page: int = Field(
        default=0,
        description="Item Count Per Page")

    order_by_column_name: str = Field(
        default="",
        description="Order By Column Name")

    order_by_descending: bool = Field(
        default=False,
        description="Order By Descending")

    success: bool = Field(
        default=False,
        description="Success")

    records_total: int = Field(
        default=0,
        description="Records Total")

    records_filtered: int = Field(
        default=0,
        description="Records Filtered")

    message: str = Field(
        default="",
        description="Message")

    app_version: str = Field(
        default="",
        description="App Version")

    validation_errors: List[ValidationErrorItem] = Field(
        default_factory=list,
        description="Validation Errors")
