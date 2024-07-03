# apis/models/pac_user_tac_list.py
# pylint: disable=unused-import

"""
This module contains the models for the
Pac User Tac List API.

- PacUserTacListGetModelRequest: Represents the
    request model for getting the
    pac Pac User Tac List Report.
- PacUserTacListGetModelResponseItem: Represents the
    response model item for the
    pac Pac User Tac List Report.
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
from reports.pac_user_tac_list import (
    ReportManagerPacUserTacList)
from reports.report_request_validation_error import \
    ReportRequestValidationError
from reports.row_models.pac_user_tac_list import (
    ReportItemPacUserTacList)


class PacUserTacListGetModelRequest(CamelModel):
    """
    Represents the request model for getting the
    pac Pac User Tac List Report.

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


    class Config:
        """
        Configuration class for the
        PacUserTacList model.

        Attributes:
            json_encoders (dict): A dictionary mapping data
            types to custom JSON encoder functions.
        """
        populate_by_name = True
        # json_encoders = {
        #     datetime: lambda v: v.isoformat()
        # }

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


class PacUserTacListGetModelResponseItem(CamelModel):
    """
    Represents the response model item for the
    pac Pac User Tac List Report.

    """
    tac_code: UUID4 = Field(
        default_factory=lambda: uuid.UUID(
            '00000000-0000-0000-0000-000000000000'
        ),
        alias="tacCode",
        description="Tac Code")
    tac_description: str = Field(
        default="",
        alias="tacDescription",
        description="Tac Description")
    tac_display_order: int = Field(
        default=0,
        alias="tacDisplayOrder",
        description="Tac Display Order")
    tac_is_active: bool = Field(
        default=False,
        alias="tacIsActive",
        description="Tac Is Active")
    tac_lookup_enum_name: str = Field(
        default="",
        alias="tacLookupEnumName",
        description="Tac Lookup Enum Name")
    tac_name: str = Field(
        default="",
        alias="tacName",
        description="Tac Name")
    pac_name: str = Field(
        default="",
        alias="pacName",
        description="Pac Name")

    def load_report_item(
            self, data: ReportItemPacUserTacList):
        """
        Loads the data from a
        ReportItemPacUserTacList
        object into the response model item.

        Args:
            data (ReportItemPacUserTacList): The
                ReportItemPacUserTacList object
                to load the data from.
        """
        self.tac_code = (
            data.tac_code)
        self.tac_description = (
            data.tac_description)
        self.tac_display_order = (
            data.tac_display_order)
        self.tac_is_active = (
            data.tac_is_active)
        self.tac_lookup_enum_name = (
            data.tac_lookup_enum_name)
        self.tac_name = (
            data.tac_name)
        self.pac_name = (
            data.pac_name)

    def build_report_item(
        self
    ) -> ReportItemPacUserTacList:
        """
        Builds a ReportItemPacUserTacList object
        from the response model item.

        Returns:
            ReportItemPacUserTacList: The built
            ReportItemPacUserTacList object.
        """

        data = ReportItemPacUserTacList()
        data.tac_code = (
            self.tac_code)
        data.tac_description = (
            self.tac_description)
        data.tac_display_order = (
            self.tac_display_order)
        data.tac_is_active = (
            self.tac_is_active)
        data.tac_lookup_enum_name = (
            self.tac_lookup_enum_name)
        data.tac_name = (
            self.tac_name)
        data.pac_name = (
            self.pac_name)
        return data


class PacUserTacListGetModelResponse(
    ListModel
):
    """
    Represents the response model for the
    PacUserTacListGetModel API.

    Attributes:
        request (PacUserTacListGetModelRequest):
            The request model for the API.
        items (List[PacUserTacListGetModelResponseItem]):
            The list of response items.
    """

    request: PacUserTacListGetModelRequest = (
        PacUserTacListGetModelRequest())
    items: List[PacUserTacListGetModelResponseItem] = Field(
        default_factory=list)

    async def process_request(
        self,
        session_context: SessionContext,
        pac_code: uuid.UUID,
        request: PacUserTacListGetModelRequest
    ):
        """
        Processes the API request and generates the response items.

        Args:
            session_context (SessionContext): The session context.
            pac_code (uuid.UUID): The pac code.
            request (PacUserTacListGetModelRequest): The request model.

        Raises:
            ReportRequestValidationError: If there is
                a validation error in the request.

        Returns:
            None
        """
        try:
            logging.info(
                "loading model..."
                "PacUserTacListGetModelResponse")
            generator = ReportManagerPacUserTacList(
                session_context)
            logging.info(
                "processing..."
                "PacUserTacListGetModelResponse")
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
                    PacUserTacListGetModelResponseItem()
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
