# apis/fs_farm_api/v1_0/endpoints/error_log_config_resolve_error_log.py
# pylint: disable=unused-import

"""
This module contains the implementation of the
ErrorLogConfigResolveErrorLogRouter,
which handles the API endpoints related to the
Error Log Config Resolve Error Log.

The ErrorLogConfigResolveErrorLogRouter provides
the following endpoints:
- GET /api/v1_0/error-log-config-resolve-error-log/...
    {error_log_code}/init:
    Get the initialization data for the
    Error Log Config Resolve Error Log page.
- GET /api/v1_0/error-log-config-resolve-error-log/...
    {error_log_code}:
    Get the Error Log Config Resolve Error Log Report
    for a specific  code.
- GET /api/v1_0/error-log-config-resolve-error-log/...
        {error_log_code}/to-csv:
    Retrieve the Error Log Config Resolve Error Log
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

ERROR_LOG_CODE = "Error Log Code"

TRACEBACK = " traceback:"

EXCEPTION_OCCURRED = "Exception occurred: %s - %s"

API_LOG_ERROR_FORMAT = "response.message: %s"


class ErrorLogConfigResolveErrorLogRouterConfig():
    """
    Configuration class for the
    ErrorLogConfigResolveErrorLogRouter.
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


class ErrorLogConfigResolveErrorLogRouter(BaseRouter):
    """
    Router class for the
    Error Log Config Resolve Error Log
    API endpoints.
    """
    router = APIRouter(tags=["ErrorLogConfigResolveErrorLog"])


    @staticmethod
    @router.post(
        "/api/v1_0/error-log-config-resolve-error-log/{error_log_code}",
        response_model=(
            api_models
            .ErrorLogConfigResolveErrorLogPostModelResponse
        ),
        summary="Error Log Config Resolve Error Log Business Flow")
    async def request_post_with_id(
        error_log_code: uuid.UUID,
        request_model: (
            api_models.ErrorLogConfigResolveErrorLogPostModelRequest),
        session: AsyncSession = Depends(get_db),
        api_key: str = Depends(api_key_header)
    ):
        """
        Error Log Config Resolve Error Log api post endpoint

        Parameters:
        - error_log_code: The code of the  object.
        - request_model: The request model containing
            the details of the item to be added.
        - session: Database session dependency.
        - api_key: API key for authorization.

        Returns:
        - response: JSON response with the result of the operation.
        """
        logging.info(
            "ErrorLogConfigResolveErrorLogRouter."
            "request_post_with_id start. errorLogCode: %s",
            error_log_code
        )
        auth_dict = BaseRouter.implementation_check(
            ErrorLogConfigResolveErrorLogRouterConfig
            .is_post_with_id_available)

        response = (api_models
                    .ErrorLogConfigResolveErrorLogPostModelResponse())

        auth_dict = BaseRouter.authorization_check(
            ErrorLogConfigResolveErrorLogRouterConfig.is_public,
            api_key)

        # Start a transaction
        async with session:
            try:
                logging.info("Start session...")
                session_context = SessionContext(auth_dict, session)
                error_log_code = session_context.check_context_code(
                    "ErrorLogCode",
                    error_log_code)

                logging.info("Request...")
                logging.info(request_model.__dict__)
                await response.process_request(
                    session_context,
                    error_log_code,
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
            'ErrorLogConfigResolveErrorLogRouter.submit get result:%s',
            response_data)
        return response

