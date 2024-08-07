# apis/fs_farm_api/v1_0/endpoints/plant_user_property_random_update.py  # pylint: disable=duplicate-code # noqa: E501
# pylint: disable=unused-import

"""
This module contains the implementation of the
PlantUserPropertyRandomUpdateRouter,
which handles the API endpoints related to the
Plant User Property Random Update.

The PlantUserPropertyRandomUpdateRouter provides
the following endpoints:
- GET /api/v1_0/plant-user-property-random-update/...
    {plant_code}/init:
    Get the initialization data for the
    Plant User Property Random Update page.
- GET /api/v1_0/plant-user-property-random-update/...
    {plant_code}:
    Get the Plant User Property Random Update Report
    for a specific  code.
- GET /api/v1_0/plant-user-property-random-update/...
        {plant_code}/to-csv:
    Retrieve the Plant User Property Random Update
    Report as a CSV file.
"""

import logging
import tempfile  # noqa: F401
import traceback
import uuid

from fastapi import APIRouter, Depends, Path  # noqa: F401
from fastapi.responses import FileResponse  # noqa: F401
from sqlalchemy.ext.asyncio import AsyncSession

import apis.models as api_models
import apis.models.init as api_init_models  # noqa: F401
import reports  # noqa: F401
from database import get_db
from helpers import SessionContext, api_key_header

from .base_router import BaseRouter

PLANT_CODE = "Plant Code"

TRACEBACK = " traceback:"

EXCEPTION_OCCURRED = "Exception occurred: %s - %s"

API_LOG_ERROR_FORMAT = "response.message: %s"


class PlantUserPropertyRandomUpdateRouterConfig():  # pylint: disable=too-few-public-methods
    """
    Configuration class for the
    PlantUserPropertyRandomUpdateRouter.
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


class PlantUserPropertyRandomUpdateRouter(BaseRouter):
    """
    Router class for the
    Plant User Property Random Update
    API endpoints.
    """
    router = APIRouter(tags=["PlantUserPropertyRandomUpdate"])


    @staticmethod
    @router.post(
        "/api/v1_0/plant-user-property-random-update"
        "/{plant_code}",
        response_model=(
            api_models
            .PlantUserPropertyRandomUpdatePostModelResponse
        ),
        summary="Plant User Property Random Update Business Flow")
    async def request_post_with_id(
        plant_code: uuid.UUID,
        request_model: (
            api_models.PlantUserPropertyRandomUpdatePostModelRequest),
        session: AsyncSession = Depends(get_db),
        api_key: str = Depends(api_key_header)
    ):
        """
        Plant User Property Random Update api post endpoint

        Parameters:
        - plant_code: The code of the  object.
        - request_model: The request model containing
            the details of the item to be added.
        - session: Database session dependency.
        - api_key: API key for authorization.

        Returns:
        - response: JSON response with the result of the operation.
        """
        logging.info(
            "PlantUserPropertyRandomUpdateRouter."
            "request_post_with_id start. plantCode: %s",
            plant_code
        )
        auth_dict = BaseRouter.implementation_check(
            PlantUserPropertyRandomUpdateRouterConfig
            .is_post_with_id_available)

        response = (api_models
                    .PlantUserPropertyRandomUpdatePostModelResponse())

        auth_dict = BaseRouter.authorization_check(
            PlantUserPropertyRandomUpdateRouterConfig.is_public,
            api_key)

        # Start a transaction
        async with session:
            try:
                logging.info(
                    "PlantUserPropertyRandomUpdateRouter."
                    "request_post_with_id "
                    "Start session...")
                session_context = SessionContext(auth_dict, session)
                plant_code = session_context.check_context_code(
                    "PlantCode",
                    plant_code)

                logging.info(
                    "PlantUserPropertyRandomUpdateRouter."
                    "request_post_with_id "
                    "Request...")
                logging.info(request_model.__dict__)
                await response.process_request(
                    session_context,
                    plant_code,
                    request_model
                )
            except TypeError as te:
                logging.info(
                    "PlantUserPropertyRandomUpdateRouter."
                    "request_post_with_id "
                    "TypeError Exception occurred")
                response.success = False
                traceback_string = "".join(
                    traceback.format_tb(te.__traceback__)
                )
                response.message = f"{te} traceback: {traceback_string}"
                logging.info(API_LOG_ERROR_FORMAT, response.message)
            except Exception as e:  # pylint: disable=broad-exception-caught
                logging.info(
                    "PlantUserPropertyRandomUpdateRouter."
                    "request_post_with_id "
                    "Exception occurred")
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
            "PlantUserPropertyRandomUpdateRouter."
            "request_post_with_id "
            "get result:%s",
            response_data)
        return response
