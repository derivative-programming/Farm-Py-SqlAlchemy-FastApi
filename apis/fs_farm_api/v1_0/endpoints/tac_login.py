# apis/fs_farm_api/v1_0/endpoints/tac_login.py  # pylint: disable=duplicate-code
# pylint: disable=unused-import

"""
This module contains the implementation of the
TacLoginRouter,
which handles the API endpoints related to the
Tac Login.

The TacLoginRouter provides
the following endpoints:
- GET /api/v1_0/tac-login/...
    {tac_code}/init:
    Get the initialization data for the
    Tac Login page.
- GET /api/v1_0/tac-login/...
    {tac_code}:
    Get the Tac Login Report
    for a specific tac code.
- GET /api/v1_0/tac-login/...
        {tac_code}/to-csv:
    Retrieve the Tac Login
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

TAC_CODE = "Tac Code"

TRACEBACK = " traceback:"

EXCEPTION_OCCURRED = "Exception occurred: %s - %s"

API_LOG_ERROR_FORMAT = "response.message: %s"


class TacLoginRouterConfig():  # pylint: disable=too-few-public-methods
    """
    Configuration class for the
    TacLoginRouter.
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
    is_public: bool = True


class TacLoginRouter(BaseRouter):
    """
    Router class for the
    Tac Login
    API endpoints.
    """
    router = APIRouter(tags=["TacLogin"])


    @staticmethod
    @router.get(
        "/api/v1_0/tac-login"
        "/{tac_code}/init",
        response_model=(
            api_init_models.
            TacLoginInitObjWFGetInitModelResponse
        ),
        summary="Tac Login Init Page")
    async def request_get_init(
        tac_code: uuid.UUID = Path(..., description=TAC_CODE),
        session: AsyncSession = Depends(get_db),
        api_key: str = Depends(api_key_header)
    ):
        """
        Get the initialization data for the
        Tac Login page.

        Args:
            tac_code (uuid.UUID): The UUID of the tac.
            session (AsyncSession): The database session.
            api_key (str): The API key for authorization.

        Returns:
            TacLoginInitObjWFGetInitModelResponse:
                The initialization data for the
                Tac Login page.
        """

        logging.info(
            "TacLoginRouter"
            ".request_get_init start. tacCode:%s",
            tac_code)
        auth_dict = BaseRouter.implementation_check(
            TacLoginRouterConfig
            .is_get_init_available)

        response = (
            api_init_models.
            TacLoginInitObjWFGetInitModelResponse()
        )

        auth_dict = BaseRouter.authorization_check(
            TacLoginRouterConfig.is_public, api_key)

        init_request = (
            api_init_models.
            TacLoginInitObjWFGetInitModelRequest()
        )

        # Start a transaction
        async with session:
            try:
                logging.info(
                    "TacLoginRouter"
                    ".request_get_init "
                    "Start session...")
                session_context = SessionContext(auth_dict, session)
                tac_code = session_context.check_context_code(
                    "TacCode",
                    tac_code
                )

                logging.info(
                    "TacLoginRouter."
                    "request_get_init "
                    "process_request...")
                response = await init_request.process_request(
                    session_context,
                    tac_code,
                    response
                )
            except TypeError as te:
                logging.info(
                    "TacLoginRouter.request_get_init"
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
            "TacLoginRouter."
            "request_get_init "
            "result:%s",
            response_data)
        return response


    @staticmethod
    @router.post(
        "/api/v1_0/tac-login"
        "/{tac_code}",
        response_model=(
            api_models
            .TacLoginPostModelResponse
        ),
        summary="Tac Login Business Flow")
    async def request_post_with_id(
        tac_code: uuid.UUID,
        request_model: (
            api_models.TacLoginPostModelRequest),
        session: AsyncSession = Depends(get_db),
        api_key: str = Depends(api_key_header)
    ):
        """
        Tac Login api post endpoint

        Parameters:
        - tac_code: The code of the tac object.
        - request_model: The request model containing
            the details of the item to be added.
        - session: Database session dependency.
        - api_key: API key for authorization.

        Returns:
        - response: JSON response with the result of the operation.
        """
        logging.info(
            "TacLoginRouter."
            "request_post_with_id start. tacCode: %s",
            tac_code
        )
        auth_dict = BaseRouter.implementation_check(
            TacLoginRouterConfig
            .is_post_with_id_available)

        response = (api_models
                    .TacLoginPostModelResponse())

        auth_dict = BaseRouter.authorization_check(
            TacLoginRouterConfig.is_public,
            api_key)

        # Start a transaction
        async with session:
            try:
                logging.info(
                    "TacLoginRouter."
                    "request_post_with_id "
                    "Start session...")
                session_context = SessionContext(auth_dict, session)
                tac_code = session_context.check_context_code(
                    "TacCode",
                    tac_code)

                logging.info(
                    "TacLoginRouter."
                    "request_post_with_id "
                    "Request...")
                logging.info(request_model.__dict__)
                await response.process_request(
                    session_context,
                    tac_code,
                    request_model
                )
            except TypeError as te:
                logging.info(
                    "TacLoginRouter."
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
                    "TacLoginRouter."
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
            "TacLoginRouter."
            "request_post_with_id "
            "get result:%s",
            response_data)
        return response
