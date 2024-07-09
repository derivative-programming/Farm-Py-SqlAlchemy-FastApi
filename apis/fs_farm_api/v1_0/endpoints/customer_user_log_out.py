# apis/fs_farm_api/v1_0/endpoints/customer_user_log_out.py  # pylint: disable=duplicate-code # noqa: E501
# pylint: disable=unused-import

"""
This module contains the implementation of the
CustomerUserLogOutRouter,
which handles the API endpoints related to the
Customer User Log Out.

The CustomerUserLogOutRouter provides
the following endpoints:
- GET /api/v1_0/customer-user-log-out/...
    {customer_code}/init:
    Get the initialization data for the
    Customer User Log Out page.
- GET /api/v1_0/customer-user-log-out/...
    {customer_code}:
    Get the Customer User Log Out Report
    for a specific customer code.
- GET /api/v1_0/customer-user-log-out/...
        {customer_code}/to-csv:
    Retrieve the Customer User Log Out
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


class CustomerUserLogOutRouterConfig():  # pylint: disable=too-few-public-methods
    """
    Configuration class for the
    CustomerUserLogOutRouter.
    """

    # constants
    is_get_available: bool = False
    is_get_with_id_available: bool = False
    is_get_init_available: bool = True
    is_get_to_csv_available: bool = False
    is_post_available: bool = False
    is_post_with_id_available: bool = True
    is_put_available: bool = False
    is_delete_available: bool = False
    is_public: bool = False


class CustomerUserLogOutRouter(BaseRouter):
    """
    Router class for the
    Customer User Log Out
    API endpoints.
    """
    router = APIRouter(tags=["CustomerUserLogOut"])


    @staticmethod
    @router.get(
        "/api/v1_0/customer-user-log-out"
        "/{customer_code}/init",
        response_model=(
            api_init_models.
            CustomerUserLogOutInitObjWFGetInitModelResponse
        ),
        summary="Customer User Log Out Init Page")
    async def request_get_init(
        customer_code: uuid.UUID = Path(..., description=CUSTOMER_CODE),
        session: AsyncSession = Depends(get_db),
        api_key: str = Depends(api_key_header)
    ):
        """
        Get the initialization data for the
        Customer User Log Out page.

        Args:
            customer_code (uuid.UUID): The UUID of the customer.
            session (AsyncSession): The database session.
            api_key (str): The API key for authorization.

        Returns:
            CustomerUserLogOutInitObjWFGetInitModelResponse:
                The initialization data for the
                Customer User Log Out page.
        """

        logging.info(
            "CustomerUserLogOutRouter"
            ".request_get_init start. customerCode:%s",
            customer_code)
        auth_dict = BaseRouter.implementation_check(
            CustomerUserLogOutRouterConfig
            .is_get_init_available)

        response = (
            api_init_models.
            CustomerUserLogOutInitObjWFGetInitModelResponse()
        )

        auth_dict = BaseRouter.authorization_check(
            CustomerUserLogOutRouterConfig.is_public, api_key)

        init_request = (
            api_init_models.
            CustomerUserLogOutInitObjWFGetInitModelRequest()
        )

        # Start a transaction
        async with session:
            try:
                logging.info(
                    "CustomerUserLogOutRouter"
                    ".request_get_init "
                    "Start session...")
                session_context = SessionContext(auth_dict, session)
                customer_code = session_context.check_context_code(
                    "CustomerCode",
                    customer_code
                )

                logging.info(
                    "CustomerUserLogOutRouter."
                    "request_get_init "
                    "process_request...")
                response = await init_request.process_request(
                    session_context,
                    customer_code,
                    response
                )
            except TypeError as te:
                logging.info(
                    "CustomerUserLogOutRouter.request_get_init"
                    " TypeError Exception occurred")
                response.success = False
                traceback_string = "".join(
                    traceback.format_tb(te.__traceback__))
                response.message = str(te) + TRACEBACK + traceback_string
            except Exception as e:  # pylint: disable=broad-exception-caught
                logging.info(
                    EXCEPTION_OCCURRED,
                    e.__class__.__name__,
                    e
                )
                response.success = False
                traceback_string = "".join(
                    traceback.format_tb(e.__traceback__))
                response.message = str(e) + TRACEBACK + traceback_string
            finally:
                if response.success is True:
                    await session.commit()
                else:
                    await session.rollback()
        response_data = response.model_dump_json()
        logging.info(
            "CustomerUserLogOutRouter."
            "request_get_init "
            "result:%s",
            response_data)
        return response


    @staticmethod
    @router.post(
        "/api/v1_0/customer-user-log-out"
        "/{customer_code}",
        response_model=(
            api_models
            .CustomerUserLogOutPostModelResponse
        ),
        summary="Customer User Log Out Business Flow")
    async def request_post_with_id(
        customer_code: uuid.UUID,
        request_model: (
            api_models.CustomerUserLogOutPostModelRequest),
        session: AsyncSession = Depends(get_db),
        api_key: str = Depends(api_key_header)
    ):
        """
        Customer User Log Out api post endpoint

        Parameters:
        - customer_code: The code of the customer object.
        - request_model: The request model containing
            the details of the item to be added.
        - session: Database session dependency.
        - api_key: API key for authorization.

        Returns:
        - response: JSON response with the result of the operation.
        """
        logging.info(
            "CustomerUserLogOutRouter."
            "request_post_with_id start. customerCode: %s",
            customer_code
        )
        auth_dict = BaseRouter.implementation_check(
            CustomerUserLogOutRouterConfig
            .is_post_with_id_available)

        response = (api_models
                    .CustomerUserLogOutPostModelResponse())

        auth_dict = BaseRouter.authorization_check(
            CustomerUserLogOutRouterConfig.is_public,
            api_key)

        # Start a transaction
        async with session:
            try:
                logging.info(
                    "CustomerUserLogOutRouter."
                    "request_post_with_id "
                    "Start session...")
                session_context = SessionContext(auth_dict, session)
                customer_code = session_context.check_context_code(
                    "CustomerCode",
                    customer_code)

                logging.info(
                    "CustomerUserLogOutRouter."
                    "request_post_with_id "
                    "Request...")
                logging.info(request_model.__dict__)
                await response.process_request(
                    session_context,
                    customer_code,
                    request_model
                )
            except TypeError as te:
                logging.info(
                    "CustomerUserLogOutRouter."
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
                    "CustomerUserLogOutRouter."
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
            "CustomerUserLogOutRouter."
            "request_post_with_id "
            "get result:%s",
            response_data)
        return response
