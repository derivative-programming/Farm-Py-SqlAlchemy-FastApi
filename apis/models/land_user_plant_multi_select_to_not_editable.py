# apis/models/land_user_plant_multi_select_to_not_editable.py
# pylint: disable=unused-import

"""
This module contains the models for the
Land User Plant Multi Select To Not Editable API.
"""

import json
import logging
import uuid  # noqa: F401
from datetime import date, datetime, timezone  # noqa: F401
from decimal import Decimal  # noqa: F401

from pydantic import UUID4, Field  # noqa: F401

from apis.models.validation_error import ValidationErrorItem
from business.land import LandBusObj
from flows.base.flow_validation_error import FlowValidationError
from flows.land_user_plant_multi_select_to_not_editable import (
    FlowLandUserPlantMultiSelectToNotEditable,
    FlowLandUserPlantMultiSelectToNotEditableResult)
from helpers import SessionContext, TypeConversion  # noqa: F401
from helpers.formatting import snake_to_camel, pascal_to_camel
from helpers.pydantic_serialization import CamelModel

from .post_reponse import PostResponse


class LandUserPlantMultiSelectToNotEditablePostModelRequest(CamelModel):
    """
    Represents the request model for the
    Land User Plant Multi Select To Not Editable API.
    """

    force_error_message: str = Field(
        default="",
        alias="forceErrorMessage",
        description="Force Error Message")
    plant_code_list_csv: str = Field(
        default="",
        alias="plantCodeListCsv",
        description="plant Code List Csv")

    class Config:
        """
        Configuration class for the
        LandUserPlantMultiSelectToNotEditablePostModelRequest.
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
        return data  # {pascal_to_camel(k): v for k, v in data.items()}

    def to_dict_camel_serialized(self):
        """
        Convert the model to a dictionary with camelCase
        keys and serialized values.
        """

        data = json.loads(self.model_dump_json(by_alias=True))
        return data  # {pascal_to_camel(k): v for k, v in data.items()}


class LandUserPlantMultiSelectToNotEditablePostModelResponse(PostResponse):
    """
    Represents the response model for the
    Land User Plant Multi Select To Not Editable API.
    """


    def load_flow_response(
            self, data: FlowLandUserPlantMultiSelectToNotEditableResult):
        """
        Loads the flow response data into the response model.
        """


    async def process_request(
        self,
        session_context: SessionContext,
        land_code: uuid.UUID,
        request: LandUserPlantMultiSelectToNotEditablePostModelRequest
    ):
        """
        Processes the request and generates the response.
        """

        try:
            logging.info(
                "loading model..."
                "LandUserPlantMultiSelectToNotEditablePostModelResponse")
            land_bus_obj = LandBusObj(session_context)
            await land_bus_obj.load_from_code(code=land_code)
            if land_bus_obj.get_land_obj() is None:
                logging.info("Invalid land_code")
                raise ValueError("Invalid land_code")
            flow = FlowLandUserPlantMultiSelectToNotEditable(
                session_context)
            logging.info(
                "process flow..."
                "LandUserPlantMultiSelectToNotEditablePostModelResponse")
            flow_response = await flow.process(
                land_bus_obj,
                request.plant_code_list_csv,
# endset  # noqa: E122
            )
            self.load_flow_response(flow_response)
            self.success = True
            self.message = "Success."
        except FlowValidationError as ve:
            logging.info(
                "error..."
                "LandUserPlantMultiSelectToNotEditablePostModelResponse")
            self.success = False
            self.validation_errors = list()
            for key in ve.error_dict:
                validation_error = ValidationErrorItem()
                validation_error.property = snake_to_camel(key)
                validation_error.message = ve.error_dict[key]
                self.validation_errors.append(validation_error)

    def to_json(self):
        """
        Converts the object to a JSON representation.

        Returns:
            str: The JSON representation of the object.
        """
        return self.model_dump_json()
