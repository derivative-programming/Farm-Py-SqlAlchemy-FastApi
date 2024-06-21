# apis/fs_farm_api/v1_0/endpoints/tac_register.py
"""
This module contains the implementation of the
TacRegisterRouter,
which handles the API endpoints related to the
Tac Register.
The TacRegisterRouter provides the following endpoints:
    - GET /api/v1_0/tac-register/{tac_code}/init:
        Get the initialization data for the
        Tac Register page.
    - GET /api/v1_0/tac-register/{tac_code}:
        Get the Tac Register Report
        for a specific tac code.
    - GET /api/v1_0/tac-register/{tac_code}/to-csv:
        Retrieve the Tac Register
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
TAC_CODE = "Tac Code"
TRACEBACK = " traceback:"
EXCEPTION_OCCURRED = "Exception occurred: %s - %s"
API_LOG_ERROR_FORMAT = "response.message: %s"
class TacRegisterRouterConfig():
    """
    Configuration class for the TacRegisterRouter.
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
class TacRegisterRouter(BaseRouter):
    """
    Router class for the
    Tac Register
    API endpoints.
    """
    router = APIRouter(tags=["TacRegister"])

    @staticmethod
    @router.get(
        "/api/v1_0/tac-register/{tac_code}/init",
        response_model=(
            api_init_models.
            TacRegisterInitObjWFGetInitModelResponse),
        summary="Tac Register Init Page")
    async def request_get_init(
        tac_code: uuid.UUID = Path(..., description=TAC_CODE),
        session: AsyncSession = Depends(get_db),
        api_key: str = Depends(api_key_header)
    ):
        """
        Get the initialization data for the
        Tac Register page.
        Args:
            tac_code (uuid.UUID): The UUID of the tac.
            session (AsyncSession): The database session.
            api_key (str): The API key for authorization.
        Returns:
            TacRegisterInitObjWFGetInitModelResponse:
                The initialization data for the
                Tac Register page.
        """
        logging.info(
            'TacRegisterRouter.request_get_init start. tacCode:%s',
            tac_code)
        auth_dict = BaseRouter.implementation_check(
            TacRegisterRouterConfig.is_get_init_available)
        response = (
            api_init_models.
            TacRegisterInitObjWFGetInitModelResponse()
        )
        auth_dict = BaseRouter.authorization_check(
            TacRegisterRouterConfig.is_public, api_key)
        # Start a transaction
        async with session:
            try:
                logging.info("Start session...")
                session_context = SessionContext(auth_dict, session)
                tac_code = session_context.check_context_code(
                    "TacCode",
                    tac_code
                )
                init_request = (
                    api_init_models.
                    TacRegisterInitObjWFGetInitModelRequest()
                )
                response = await init_request.process_request(
                    session_context,
                    tac_code,
                    response
                )
            except TypeError as te:
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
        logging.info('TacRegisterRouter.init get result:%s',
                     response_data)
        return response

    @staticmethod
    @router.post(
        "/api/v1_0/tac-register/{tac_code}",
        response_model=api_models.TacRegisterPostModelResponse,
        summary="Tac Register Business Flow")
    async def request_post_with_id(
        tac_code: uuid.UUID,
        request_model: api_models.TacRegisterPostModelRequest,
        session: AsyncSession = Depends(get_db),
        api_key: str = Depends(api_key_header)
    ):
        """
        Tac Register api post endpoint
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
            "TacRegisterRouter."
            "request_post_with_id start. tacCode: %s",
            tac_code
        )
        auth_dict = BaseRouter.implementation_check(
            TacRegisterRouterConfig.is_post_with_id_available)
        response = api_models.TacRegisterPostModelResponse()
        auth_dict = BaseRouter.authorization_check(
            TacRegisterRouterConfig.is_public,
            api_key)
        # Start a transaction
        async with session:
            try:
                logging.info("Start session...")
                session_context = SessionContext(auth_dict, session)
                tac_code = session_context.check_context_code(
                    "TacCode",
                    tac_code)
                logging.info("Request...")
                logging.info(request_model.__dict__)
                await response.process_request(
                    session_context,
                    tac_code,
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
            'TacRegisterRouter.submit get result:%s',
            response_data)
        return response

