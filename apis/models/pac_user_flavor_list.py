# apis/models/pac_user_flavor_list.py
# pylint: disable=unused-import

"""
This module contains the models for the
Pac User Flavor List API.

- PacUserFlavorListGetModelRequest: Represents the
    request model for getting the
    pac Pac User Flavor List Report.
- PacUserFlavorListGetModelResponseItem: Represents the
    response model item for the
    pac Pac User Flavor List Report.
"""

import json
import logging
import uuid  # noqa: F401
from datetime import date, datetime  # noqa: F401
from decimal import Decimal  # noqa: F401
from typing import List

from pydantic import UUID4, Field

from apis.models.list_model import ListModel
from apis.models.validation_error import ValidationErrorItem
from helpers import SessionContext, TypeConversion
from helpers.formatting import snake_to_camel
from helpers.pydantic_serialization import CamelModel
from reports.pac_user_flavor_list import (
    ReportManagerPacUserFlavorList)
from reports.report_request_validation_error import \
    ReportRequestValidationError
from reports.row_models.pac_user_flavor_list import (
    ReportItemPacUserFlavorList)


class PacUserFlavorListGetModelRequest(CamelModel):
    """
    Represents the request model for getting the
    pac Pac User Flavor List Report.

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
    force_error_message: str = Field(
        default="",
        description="Force Error Message")


    class Config:
        """
        Configuration class for the
        PacUserFlavorList model.

        Attributes:
            json_encoders (dict): A dictionary mapping data
            types to custom JSON encoder functions.
        """
        json_encoders = {
            datetime: lambda v: v.isoformat()
        }

    def to_dict_snake(self):
        """
        Convert the model to a dictionary with snake_case keys.
        """
        data = self.model_dump()
        return data

    def to_dict_snake_serialized(self):
        """
        Convert the model to a dictionary with snake_case
        keys and serialized values.
        """
        data = json.loads(self.model_dump_json())
        return data

    def to_dict_camel(self):
        """
        Convert the model to a dictionary with camelCase keys.
        """
        data = self.model_dump()
        return {snake_to_camel(k): v for k, v in data.items()}

    def to_dict_camel_serialized(self):
        """
        Convert the model to a dictionary with camelCase
        keys and serialized values.
        """
        data = json.loads(self.model_dump_json())
        return {snake_to_camel(k): v for k, v in data.items()}


class PacUserFlavorListGetModelResponseItem(CamelModel):
    """
    Represents the response model item for the
    pac Pac User Flavor List Report.

    """
    flavor_code: UUID4 = Field(
        default_factory=lambda: uuid.UUID(
            '00000000-0000-0000-0000-000000000000'
        ),
        description="Flavor Code")
    flavor_description: str = Field(
        default="",
        description="Flavor Description")
    flavor_display_order: int = Field(
        default=0,
        description="Flavor Display Order")
    flavor_is_active: bool = Field(
        default=False,
        description="Flavor Is Active")
    flavor_lookup_enum_name: str = Field(
        default="",
        description="Flavor Lookup Enum Name")
    flavor_name: str = Field(
        default="",
        description="Flavor Name")
    pac_name: str = Field(
        default="",
        description="Pac Name")

    def load_report_item(
            self, data: ReportItemPacUserFlavorList):
        """
        Loads the data from a
        ReportItemPacUserFlavorList
        object into the response model item.

        Args:
            data (ReportItemPacUserFlavorList): The
                ReportItemPacUserFlavorList object
                to load the data from.
        """
        self.flavor_code = (
            data.flavor_code)
        self.flavor_description = (
            data.flavor_description)
        self.flavor_display_order = (
            data.flavor_display_order)
        self.flavor_is_active = (
            data.flavor_is_active)
        self.flavor_lookup_enum_name = (
            data.flavor_lookup_enum_name)
        self.flavor_name = (
            data.flavor_name)
        self.pac_name = (
            data.pac_name)

    def build_report_item(
        self
    ) -> ReportItemPacUserFlavorList:
        """
        Builds a ReportItemPacUserFlavorList object
        from the response model item.

        Returns:
            ReportItemPacUserFlavorList: The built
            ReportItemPacUserFlavorList object.
        """

        data = ReportItemPacUserFlavorList()
        data.flavor_code = (
            self.flavor_code)
        data.flavor_description = (
            self.flavor_description)
        data.flavor_display_order = (
            self.flavor_display_order)
        data.flavor_is_active = (
            self.flavor_is_active)
        data.flavor_lookup_enum_name = (
            self.flavor_lookup_enum_name)
        data.flavor_name = (
            self.flavor_name)
        data.pac_name = (
            self.pac_name)
        return data


class PacUserFlavorListGetModelResponse(ListModel):
    """
    Represents the response model for the
    PacUserFlavorListGetModel API.

    Attributes:
        request (PacUserFlavorListGetModelRequest):
            The request model for the API.
        items (List[PacUserFlavorListGetModelResponseItem]):
            The list of response items.
    """

    request: PacUserFlavorListGetModelRequest = PacUserFlavorListGetModelRequest()
    items: List[PacUserFlavorListGetModelResponseItem] = Field(
        default_factory=list)

    async def process_request(
        self,
        session_context: SessionContext,
        pac_code: uuid.UUID,
        request: PacUserFlavorListGetModelRequest
    ):
        """
        Processes the API request and generates the response items.

        Args:
            session_context (SessionContext): The session context.
            pac_code (uuid.UUID): The pac code.
            request (PacUserFlavorListGetModelRequest): The request model.

        Raises:
            ReportRequestValidationError: If there is
                a validation error in the request.

        Returns:
            None
        """
        try:
            logging.info(
                "loading model..."
                "PacUserFlavorListGetModelResponse")
            generator = ReportManagerPacUserFlavorList(
                session_context)
            logging.info(
                "processing..."
                "PacUserFlavorListGetModelResponse")
            items = await generator.generate(
                pac_code,

# endset  # noqa: E122
                request.page_number,
                request.item_count_per_page,
                request.order_by_column_name,
                request.order_by_descending
            )
            self.items = list()
            for item in items:
                report_item = \
                    PacUserFlavorListGetModelResponseItem()
                report_item.load_report_item(item)
                self.items.append(report_item)
            self.success = True
            self.message = "Success."
        except ReportRequestValidationError as ve:
            self.success = False
            self.message = "Validation Error..."
            self.validation_errors = list()

            error_messages = []

            for key, value in ve.error_dict.items():
                error_messages.append(value)
                validation_error = ValidationErrorItem()
                validation_error.property = snake_to_camel(key)
                validation_error.message = value
                self.validation_errors.append(validation_error)

            self.message = ','.join(error_messages)

    def to_json(self):
        """
        Converts the response model to JSON.

        Returns:
            str: The JSON representation of the response model.
        """
        return self.model_dump_json()
