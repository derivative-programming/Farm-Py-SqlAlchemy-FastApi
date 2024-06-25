# apis/fs_farm_api/v1_0/endpoints/land_user_plant_multi_select_to_not_editable.py
# pylint: disable=unused-import

"""
This module contains the implementation of the
LandUserPlantMultiSelectToNotEditableRouter,
which handles the API endpoints related to the
Land User Plant Multi Select To Not Editable.

The LandUserPlantMultiSelectToNotEditableRouter provides
the following endpoints:
- GET /api/v1_0/land-user-plant-multi-select-to-not-editable/...
    {land_code}/init:
    Get the initialization data for the
    Land User Plant Multi Select To Not Editable page.
- GET /api/v1_0/land-user-plant-multi-select-to-not-editable/...
    {land_code}:
    Get the Land User Plant Multi Select To Not Editable Report
    for a specific  code.
- GET /api/v1_0/land-user-plant-multi-select-to-not-editable/...
        {land_code}/to-csv:
    Retrieve the Land User Plant Multi Select To Not Editable
    Report as a CSV file.
"""

import logging
import tempfile
import traceback
import uuid

from fastapi import APIRouter, Depends, Path
from fastapi.responses import FileResponse
from sqlalchemy.ext.asyncio import AsyncSession

import apis.models as api_models
import apis.models.init as api_init_models
import reports
from database import get_db
from helpers import SessionContext, api_key_header

from .base_router import BaseRouter

LAND_CODE = "Land Code"

TRACEBACK = " traceback:"

EXCEPTION_OCCURRED = "Exception occurred: %s - %s"

API_LOG_ERROR_FORMAT = "response.message: %s"


class LandUserPlantMultiSelectToNotEditableRouterConfig():
    """
    Configuration class for the
    LandUserPlantMultiSelectToNotEditableRouter.
    """

    # constants
    is_get_available: bool = False
    is_get_with_id_available: bool = False
    is_get_init_available: bool = False
    is_get_to_csv_available: bool = False
    is_post_available: bool = False
    is_post_with_id_available: bool = True
    is_put_available: bool = False
    is_delete_available: bool = False
    is_public: bool = False


class LandUserPlantMultiSelectToNotEditableRouter(BaseRouter):
    """
    Router class for the
    Land User Plant Multi Select To Not Editable
    API endpoints.
    """
    router = APIRouter(tags=["LandUserPlantMultiSelectToNotEditable"])


    @staticmethod
    @router.post(
        "/api/v1_0/land-user-plant-multi-select-to-not-editable/{land_code}",
        response_model=(
            api_models
            .LandUserPlantMultiSelectToNotEditablePostModelResponse
        ),
        summary="Land User Plant Multi Select To Not Editable Business Flow")
    async def request_post_with_id(
        land_code: uuid.UUID,
        request_model: (
            api_models.LandUserPlantMultiSelectToNotEditablePostModelRequest),
        session: AsyncSession = Depends(get_db),
        api_key: str = Depends(api_key_header)
    ):
        """
        Land User Plant Multi Select To Not Editable api post endpoint

        Parameters:
        - land_code: The code of the  object.
        - request_model: The request model containing
            the details of the item to be added.
        - session: Database session dependency.
        - api_key: API key for authorization.

        Returns:
        - response: JSON response with the result of the operation.
        """
        logging.info(
            "LandUserPlantMultiSelectToNotEditableRouter."
            "request_post_with_id start. landCode: %s",
            land_code
        )
        auth_dict = BaseRouter.implementation_check(
            LandUserPlantMultiSelectToNotEditableRouterConfig
            .is_post_with_id_available)

        response = (api_models
                    .LandUserPlantMultiSelectToNotEditablePostModelResponse())

        auth_dict = BaseRouter.authorization_check(
            LandUserPlantMultiSelectToNotEditableRouterConfig.is_public,
            api_key)

        # Start a transaction
        async with session:
            try:
                logging.info("Start session...")
                session_context = SessionContext(auth_dict, session)
                land_code = session_context.check_context_code(
                    "LandCode",
                    land_code)

                logging.info("Request...")
                logging.info(request_model.__dict__)
                await response.process_request(
                    session_context,
                    land_code,
                    request_model
                )
            except TypeError as te:
                logging.info("TypeError Exception occurred")
                response.success = False
                traceback_string = "".join(
                    traceback.format_tb(te.__traceback__)
                )
                response.message = f"{te} traceback: {traceback_string}"
                logging.info(API_LOG_ERROR_FORMAT, response.message)
            except Exception as e:  # pylint: disable=broad-exception-caught
                logging.info("Exception occurred")
                response.success = False
                traceback_string = "".join(
                    traceback.format_tb(e.__traceback__)
                )
                response.message = f"{e} traceback: {traceback_string}"
                logging.info(API_LOG_ERROR_FORMAT, response.message)
            finally:
                if response.success is True:
                    await session.commit()
                else:
                    await session.rollback()
        response_data = response.model_dump_json()
        logging.info(
            'LandUserPlantMultiSelectToNotEditableRouter.submit get result:%s',
            response_data)
        return response

