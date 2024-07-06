# apis/fs_farm_api/v1_0/endpoints/customer_build_temp_api_key.py  # pylint: disable=duplicate-code
# pylint: disable=unused-import

"""
This module contains the implementation of the
CustomerBuildTempApiKeyRouter,
which handles the API endpoints related to the
Customer Build Temp Api Key.

The CustomerBuildTempApiKeyRouter provides
the following endpoints:
- GET /api/v1_0/customer-build-temp-api-key/...
    {customer_code}/init:
    Get the initialization data for the
    Customer Build Temp Api Key page.
- GET /api/v1_0/customer-build-temp-api-key/...
    {customer_code}:
    Get the Customer Build Temp Api Key Report
    for a specific  code.
- GET /api/v1_0/customer-build-temp-api-key/...
        {customer_code}/to-csv:
    Retrieve the Customer Build Temp Api Key
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

CUSTOMER_CODE = "Customer Code"

TRACEBACK = " traceback:"

EXCEPTION_OCCURRED = "Exception occurred: %s - %s"

API_LOG_ERROR_FORMAT = "response.message: %s"


class CustomerBuildTempApiKeyRouterConfig():  # pylint: disable=too-few-public-methods
    """
    Configuration class for the
    CustomerBuildTempApiKeyRouter.
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


class CustomerBuildTempApiKeyRouter(BaseRouter):
    """
    Router class for the
    Customer Build Temp Api Key
    API endpoints.
    """
    router = APIRouter(tags=["CustomerBuildTempApiKey"])


    @staticmethod
    @router.post(
        "/api/v1_0/customer-build-temp-api-key"
        "/{customer_code}",
        response_model=(
            api_models
            .CustomerBuildTempApiKeyPostModelResponse
        ),
        summary="Customer Build Temp Api Key Business Flow")
    async def request_post_with_id(
        customer_code: uuid.UUID,
        request_model: (
            api_models.CustomerBuildTempApiKeyPostModelRequest),
        session: AsyncSession = Depends(get_db),
        api_key: str = Depends(api_key_header)
    ):
        """
        Customer Build Temp Api Key api post endpoint

        Parameters:
        - customer_code: The code of the  object.
        - request_model: The request model containing
            the details of the item to be added.
        - session: Database session dependency.
        - api_key: API key for authorization.

        Returns:
        - response: JSON response with the result of the operation.
        """
        logging.info(
            "CustomerBuildTempApiKeyRouter."
            "request_post_with_id start. customerCode: %s",
            customer_code
        )
        auth_dict = BaseRouter.implementation_check(
            CustomerBuildTempApiKeyRouterConfig
            .is_post_with_id_available)

        response = (api_models
                    .CustomerBuildTempApiKeyPostModelResponse())

        auth_dict = BaseRouter.authorization_check(
            CustomerBuildTempApiKeyRouterConfig.is_public,
            api_key)

        # Start a transaction
        async with session:
            try:
                logging.info("Start session...")
                session_context = SessionContext(auth_dict, session)
                customer_code = session_context.check_context_code(
                    "CustomerCode",
                    customer_code)

                logging.info("Request...")
                logging.info(request_model.__dict__)
                await response.process_request(
                    session_context,
                    customer_code,
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
            "CustomerBuildTempApiKeyRouter"
            ".submit get result:%s",
            response_data)
        return response
