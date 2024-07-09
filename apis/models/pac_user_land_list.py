# apis/models/pac_user_land_list.py  # pylint: disable=duplicate-code # noqa: E501
# pylint: disable=unused-import

"""
This module contains the models for the
Pac User Land List API.

- PacUserLandListGetModelRequest: Represents the
    request model for getting the
    pac Pac User Land List Report.
- PacUserLandListGetModelResponseItem: Represents the
    response model item for the
    pac Pac User Land List Report.
"""

import json
import logging
import uuid  # noqa: F401
from datetime import date, datetime, timezone  # noqa: F401
from decimal import Decimal  # noqa: F401
from typing import List

from pydantic import UUID4, Field

from apis.models.list_model import ListModel
from apis.models.validation_error import ValidationErrorItem
from helpers import SessionContext, TypeConversion  # noqa: F401
from helpers.formatting import snake_to_camel
from helpers.pydantic_serialization import CamelModel
from reports.pac_user_land_list import (
    ReportManagerPacUserLandList)
from reports.report_request_validation_error import \
    ReportRequestValidationError
from reports.row_models.pac_user_land_list import (
    ReportItemPacUserLandList)


class PacUserLandListGetModelRequest(CamelModel):
    """
    Represents the request model for getting the
    pac Pac User Land List Report.

    """

    page_number: int = Field(
        default=0,
        alias="pageNumber",
        description="Page Number")
    item_count_per_page: int = Field(
        default=0,
        alias="itemCountPerPage",
        description="Item Count Per Page")
    order_by_column_name: str = Field(
        default="",
        alias="orderByColumnName",
        description="Order By Column Name")
    order_by_descending: bool = Field(
        default=False,
        alias="orderByDescending",
        description="Order By Descending")
    force_error_message: str = Field(
        default="",
        alias="forceErrorMessage",
        description="Force Error Message")


    class Config:  # pylint: disable=too-few-public-methods
        """
        Configuration class for the
        PacUserLandList model.

        Attributes:
            json_encoders (dict): A dictionary mapping data
            types to custom JSON encoder functions.
        """
        populate_by_name = True

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
        data = self.model_dump(by_alias=True)
        return data  # {snake_to_camel(k): v for k, v in data.items()}

    def to_dict_camel_serialized(self):
        """
        Convert the model to a dictionary with camelCase
        keys and serialized values.
        """
        data = json.loads(self.model_dump_json(by_alias=True))
        return data  # {snake_to_camel(k): v for k, v in data.items()}


class PacUserLandListGetModelResponseItem(CamelModel):
    """
    Represents the response model item for the
    pac Pac User Land List Report.

    """
    land_code: UUID4 = Field(
        default_factory=lambda: uuid.UUID(
            '00000000-0000-0000-0000-000000000000'
        ),
        alias="landCode",
        description="Land Code")
    land_description: str = Field(
        default="",
        alias="landDescription",
        description="Land Description")
    land_display_order: int = Field(
        default=0,
        alias="landDisplayOrder",
        description="Land Display Order")
    land_is_active: bool = Field(
        default=False,
        alias="landIsActive",
        description="Land Is Active")
    land_lookup_enum_name: str = Field(
        default="",
        alias="landLookupEnumName",
        description="Land Lookup Enum Name")
    land_name: str = Field(
        default="",
        alias="landName",
        description="Land Name")
    pac_name: str = Field(
        default="",
        alias="pacName",
        description="Pac Name")

    def load_report_item(
            self, data: ReportItemPacUserLandList):
        """
        Loads the data from a
        ReportItemPacUserLandList
        object into the response model item.

        Args:
            data (ReportItemPacUserLandList): The
                ReportItemPacUserLandList object
                to load the data from.
        """
        self.land_code = (
            data.land_code)
        self.land_description = (
            data.land_description)
        self.land_display_order = (
            data.land_display_order)
        self.land_is_active = (
            data.land_is_active)
        self.land_lookup_enum_name = (
            data.land_lookup_enum_name)
        self.land_name = (
            data.land_name)
        self.pac_name = (
            data.pac_name)

    def build_report_item(
        self
    ) -> ReportItemPacUserLandList:
        """
        Builds a ReportItemPacUserLandList object
        from the response model item.

        Returns:
            ReportItemPacUserLandList: The built
            ReportItemPacUserLandList object.
        """

        data = ReportItemPacUserLandList()
        data.land_code = (
            self.land_code)
        data.land_description = (
            self.land_description)
        data.land_display_order = (
            self.land_display_order)
        data.land_is_active = (
            self.land_is_active)
        data.land_lookup_enum_name = (
            self.land_lookup_enum_name)
        data.land_name = (
            self.land_name)
        data.pac_name = (
            self.pac_name)
        return data


class PacUserLandListGetModelResponse(
    ListModel
):
    """
    Represents the response model for the
    PacUserLandListGetModel API.

    Attributes:
        request (PacUserLandListGetModelRequest):
            The request model for the API.
        items (List[PacUserLandListGetModelResponseItem]):
            The list of response items.
    """

    request: PacUserLandListGetModelRequest = (
        PacUserLandListGetModelRequest())
    items: List[PacUserLandListGetModelResponseItem] = Field(
        default_factory=list)

    async def process_request(
        self,
        session_context: SessionContext,
        pac_code: uuid.UUID,
        request: PacUserLandListGetModelRequest
    ):  # pylint: disable=unused-argument
        """
        Processes the API request and generates the response items.

        Args:
            session_context (SessionContext): The session context.
            pac_code (uuid.UUID): The pac code.
            request (PacUserLandListGetModelRequest): The request model.

        Raises:
            ReportRequestValidationError: If there is
                a validation error in the request.

        Returns:
            None
        """
        try:
            logging.info(
                "loading model..."
                "PacUserLandListGetModelResponse")
            generator = ReportManagerPacUserLandList(
                session_context)
            logging.info(
                "processing..."
                "PacUserLandListGetModelResponse")
            items = await generator.generate(
                pac_code,

# endset  # noqa: E122
                request.page_number,
                request.item_count_per_page,
                request.order_by_column_name,
                request.order_by_descending
            )
            self.items = []
            for item in items:
                report_item = \
                    PacUserLandListGetModelResponseItem()
                report_item.load_report_item(item)
                self.items.append(report_item)
            self.success = True
            self.message = "Success."
        except ReportRequestValidationError as ve:
            self.success = False
            self.message = "Validation Error..."
            self.validation_errors = []

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
