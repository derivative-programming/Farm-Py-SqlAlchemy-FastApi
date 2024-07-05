# apis/models/pac_user_role_list.py
# pylint: disable=unused-import

"""
This module contains the models for the
Pac User Role List API.

- PacUserRoleListGetModelRequest: Represents the
    request model for getting the
    pac Pac User Role List Report.
- PacUserRoleListGetModelResponseItem: Represents the
    response model item for the
    pac Pac User Role List Report.
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
from reports.pac_user_role_list import (
    ReportManagerPacUserRoleList)
from reports.report_request_validation_error import \
    ReportRequestValidationError
from reports.row_models.pac_user_role_list import (
    ReportItemPacUserRoleList)


class PacUserRoleListGetModelRequest(CamelModel):
    """
    Represents the request model for getting the
    pac Pac User Role List Report.

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
        PacUserRoleList model.

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


class PacUserRoleListGetModelResponseItem(CamelModel):
    """
    Represents the response model item for the
    pac Pac User Role List Report.

    """
    role_code: UUID4 = Field(
        default_factory=lambda: uuid.UUID(
            '00000000-0000-0000-0000-000000000000'
        ),
        alias="roleCode",
        description="Role Code")
    role_description: str = Field(
        default="",
        alias="roleDescription",
        description="Role Description")
    role_display_order: int = Field(
        default=0,
        alias="roleDisplayOrder",
        description="Role Display Order")
    role_is_active: bool = Field(
        default=False,
        alias="roleIsActive",
        description="Role Is Active")
    role_lookup_enum_name: str = Field(
        default="",
        alias="roleLookupEnumName",
        description="Role Lookup Enum Name")
    role_name: str = Field(
        default="",
        alias="roleName",
        description="Role Name")
    pac_name: str = Field(
        default="",
        alias="pacName",
        description="Pac Name")

    def load_report_item(
            self, data: ReportItemPacUserRoleList):
        """
        Loads the data from a
        ReportItemPacUserRoleList
        object into the response model item.

        Args:
            data (ReportItemPacUserRoleList): The
                ReportItemPacUserRoleList object
                to load the data from.
        """
        self.role_code = (
            data.role_code)
        self.role_description = (
            data.role_description)
        self.role_display_order = (
            data.role_display_order)
        self.role_is_active = (
            data.role_is_active)
        self.role_lookup_enum_name = (
            data.role_lookup_enum_name)
        self.role_name = (
            data.role_name)
        self.pac_name = (
            data.pac_name)

    def build_report_item(
        self
    ) -> ReportItemPacUserRoleList:
        """
        Builds a ReportItemPacUserRoleList object
        from the response model item.

        Returns:
            ReportItemPacUserRoleList: The built
            ReportItemPacUserRoleList object.
        """

        data = ReportItemPacUserRoleList()
        data.role_code = (
            self.role_code)
        data.role_description = (
            self.role_description)
        data.role_display_order = (
            self.role_display_order)
        data.role_is_active = (
            self.role_is_active)
        data.role_lookup_enum_name = (
            self.role_lookup_enum_name)
        data.role_name = (
            self.role_name)
        data.pac_name = (
            self.pac_name)
        return data


class PacUserRoleListGetModelResponse(
    ListModel
):
    """
    Represents the response model for the
    PacUserRoleListGetModel API.

    Attributes:
        request (PacUserRoleListGetModelRequest):
            The request model for the API.
        items (List[PacUserRoleListGetModelResponseItem]):
            The list of response items.
    """

    request: PacUserRoleListGetModelRequest = (
        PacUserRoleListGetModelRequest())
    items: List[PacUserRoleListGetModelResponseItem] = Field(
        default_factory=list)

    async def process_request(
        self,
        session_context: SessionContext,
        pac_code: uuid.UUID,
        request: PacUserRoleListGetModelRequest
    ):
        """
        Processes the API request and generates the response items.

        Args:
            session_context (SessionContext): The session context.
            pac_code (uuid.UUID): The pac code.
            request (PacUserRoleListGetModelRequest): The request model.

        Raises:
            ReportRequestValidationError: If there is
                a validation error in the request.

        Returns:
            None
        """
        try:
            logging.info(
                "loading model..."
                "PacUserRoleListGetModelResponse")
            generator = ReportManagerPacUserRoleList(
                session_context)
            logging.info(
                "processing..."
                "PacUserRoleListGetModelResponse")
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
                    PacUserRoleListGetModelResponseItem()
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
