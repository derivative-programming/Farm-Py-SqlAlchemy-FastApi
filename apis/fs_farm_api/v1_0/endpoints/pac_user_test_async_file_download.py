# apis/fs_farm_api/v1_0/endpoints/pac_user_test_async_file_download.py  # pylint: disable=duplicate-code # noqa: E501
# pylint: disable=unused-import

"""
This module contains the implementation of the
PacUserTestAsyncFileDownloadRouter,
which handles the API endpoints related to the
Pac User Test Async File Download.

The PacUserTestAsyncFileDownloadRouter provides
the following endpoints:
- GET /api/v1_0/pac-user-test-async-file-download/...
    {pac_code}/init:
    Get the initialization data for the
    Pac User Test Async File Download page.
- GET /api/v1_0/pac-user-test-async-file-download/...
    {pac_code}:
    Get the Pac User Test Async File Download Report
    for a specific  code.
- GET /api/v1_0/pac-user-test-async-file-download/...
        {pac_code}/to-csv:
    Retrieve the Pac User Test Async File Download
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

PAC_CODE = "Pac Code"

TRACEBACK = " traceback:"

EXCEPTION_OCCURRED = "Exception occurred: %s - %s"

API_LOG_ERROR_FORMAT = "response.message: %s"


class PacUserTestAsyncFileDownloadRouterConfig():  # pylint: disable=too-few-public-methods
    """
    Configuration class for the
    PacUserTestAsyncFileDownloadRouter.
    """

    # constants
    is_get_available: bool = False
    is_get_with_id_available: bool = False
    is_get_init_available: bool = False
    is_get_to_csv_available: bool = False
    is_post_available: bool = False
    is_post_with_id_available: bool = True
    is_put_available: bool = True
    is_delete_available: bool = False
    is_public: bool = False


class PacUserTestAsyncFileDownloadRouter(BaseRouter):
    """
    Router class for the
    Pac User Test Async File Download
    API endpoints.
    """
    router = APIRouter(tags=["PacUserTestAsyncFileDownload"])


    @staticmethod
    @router.post(
        "/api/v1_0/pac-user-test-async-file-download"
        "/{pac_code}",
        response_model=(
            api_models
            .PacUserTestAsyncFileDownloadPostModelResponse
        ),
        summary="Pac User Test Async File Download Business Flow")
    async def request_post_with_id(
        pac_code: uuid.UUID,
        request_model: (
            api_models.PacUserTestAsyncFileDownloadPostModelRequest),
        session: AsyncSession = Depends(get_db),
        api_key: str = Depends(api_key_header)
    ):
        """
        Pac User Test Async File Download api post endpoint

        Parameters:
        - pac_code: The code of the  object.
        - request_model: The request model containing
            the details of the item to be added.
        - session: Database session dependency.
        - api_key: API key for authorization.

        Returns:
        - response: JSON response with the result of the operation.
        """
        logging.info(
            "PacUserTestAsyncFileDownloadRouter."
            "request_post_with_id start. pacCode: %s",
            pac_code
        )
        auth_dict = BaseRouter.implementation_check(
            PacUserTestAsyncFileDownloadRouterConfig
            .is_post_with_id_available)

        response = (api_models
                    .PacUserTestAsyncFileDownloadPostModelResponse())

        auth_dict = BaseRouter.authorization_check(
            PacUserTestAsyncFileDownloadRouterConfig.is_public,
            api_key)

        # Start a transaction
        async with session:
            try:
                logging.info(
                    "PacUserTestAsyncFileDownloadRouter."
                    "request_post_with_id "
                    "Start session...")
                session_context = SessionContext(auth_dict, session)
                pac_code = session_context.check_context_code(
                    "PacCode",
                    pac_code)

                logging.info(
                    "PacUserTestAsyncFileDownloadRouter."
                    "request_post_with_id "
                    "Request...")
                logging.info(request_model.__dict__)
                await response.process_request(
                    session_context,
                    pac_code,
                    request_model
                )
            except TypeError as te:
                logging.info(
                    "PacUserTestAsyncFileDownloadRouter."
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
                    "PacUserTestAsyncFileDownloadRouter."
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
            "PacUserTestAsyncFileDownloadRouter."
            "request_post_with_id "
            "get result:%s",
            response_data)
        return response
